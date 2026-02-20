"""Image analyzer — inspects metadata for a specific tag."""

from __future__ import annotations

import json
import logging
import subprocess
from typing import Any

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)

# Manifest media types indicating a multi-arch manifest list.
_INDEX_TYPES = {
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.index.v1+json",
}

# Manifest media types for a single-platform manifest.
_MANIFEST_TYPES = {
    "application/vnd.docker.distribution.manifest.v2+json",
    "application/vnd.oci.image.manifest.v1+json",
}


class ImageAnalyzer(BaseAnalyzer):
    """Inspect image metadata for a given tag using Skopeo. Resolves multi-arch manifests and reports per-platform details."""

    name = "image"
    schema_file = "image.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        """Return a report with image metadata for *tag* using skopeo."""
        # 'registry-1.docker.io' -> 'docker.io' for skopeo compatibility
        registry = client.registry
        if registry == "registry-1.docker.io":
            registry = "docker.io"

        target = f"docker://{registry}/{repository}:{tag}"

        try:
            raw_stdout = self._run_skopeo(client, ["inspect", "--raw", target])
            manifest = json.loads(raw_stdout)
        except subprocess.CalledProcessError as e:
            msg = f"Skopeo inspect failed for {target}: {e.stderr}"
            logger.error(msg)
            from regis_cli.analyzers.base import AnalyzerError

            raise AnalyzerError(msg) from e
        except Exception as e:
            msg = f"Failed to parse skopeo output for {target}: {e}"
            logger.error(msg)
            from regis_cli.analyzers.base import AnalyzerError

            raise AnalyzerError(msg) from e

        media_type = manifest.get("mediaType", "")
        platforms: list[dict[str, Any]] = []

        if media_type in _INDEX_TYPES:
            # Multi-arch image — iterate over each platform manifest.
            for entry in manifest.get("manifests", []):
                platform_info = entry.get("platform", {})
                digest = entry.get("digest", "")
                detail = self._inspect_platform(
                    client, registry, repository, digest, platform_info
                )
                platforms.append(detail)
        elif media_type in _MANIFEST_TYPES:
            # Single-platform manifest.
            detail = self._inspect_platform(client, registry, repository, tag, {})
            detail["layers_count"] = len(manifest.get("layers", []))
            platforms.append(detail)
        else:
            # Best-effort fallback for unknown media types.
            logger.warning("Unknown manifest mediaType: %s", media_type)
            detail = self._inspect_platform(client, registry, repository, tag, {})
            detail["layers_count"] = len(manifest.get("layers", []))
            platforms.append(detail)

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "platforms": platforms,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _run_skopeo(client: RegistryClient, args: list[str]) -> str:
        """Run skopeo with the given arguments, injecting credentials if present."""
        cmd = ["skopeo"] + args
        if client.username and client.password:
            cmd.extend(["--creds", f"{client.username}:{client.password}"])

        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout

    def _inspect_platform(
        self,
        client: RegistryClient,
        registry: str,
        repository: str,
        ref: str,
        platform_info: dict[str, Any],
    ) -> dict[str, Any]:
        """Inspect a single platform by running skopeo inspect --config."""
        result: dict[str, Any] = {
            "architecture": platform_info.get("architecture", "unknown"),
            "os": platform_info.get("os", "unknown"),
        }

        if ref.startswith("sha256:"):
            result["digest"] = ref
            target = f"docker://{registry}/{repository}@{ref}"
        else:
            target = f"docker://{registry}/{repository}:{ref}"

        if "variant" in platform_info:
            result["variant"] = platform_info["variant"]

        args = ["inspect", "--config"]
        if result["os"] != "unknown":
            args.extend(["--override-os", result["os"]])
        if result["architecture"] != "unknown":
            args.extend(["--override-arch", result["architecture"]])
        args.append(target)

        try:
            config_stdout = self._run_skopeo(client, args)
            config = json.loads(config_stdout)
            result["created"] = config.get("created")
            result["labels"] = config.get("config", {}).get("Labels") or {}

            if result["architecture"] == "unknown":
                result["architecture"] = config.get("architecture", "unknown")
            if result["os"] == "unknown":
                result["os"] = config.get("os", "unknown")

            # Fetch layers count for multi-arch variants by fetching the variant manifest
            if ref.startswith("sha256:"):
                raw_stdout = self._run_skopeo(client, ["inspect", "--raw", target])
                plat_manifest = json.loads(raw_stdout)
                result["layers_count"] = len(plat_manifest.get("layers", []))

        except subprocess.CalledProcessError as e:
            logger.debug("Skopeo command failed for %s: %s", target, e.stderr)
        except Exception:
            logger.debug("Could not inspect platform %s", target, exc_info=True)

        return result
