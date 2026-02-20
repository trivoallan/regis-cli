"""Skopeo analyzer — provides raw image metadata and platform details using skopeo."""

from __future__ import annotations

import json
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from regis_cli.analyzers.base import AnalyzerError, BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)

# Manifest media types indicating a multi-arch manifest list.
_INDEX_TYPES = {
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.index.v1+json",
}

# Default timeout for Skopeo calls (seconds)
DEFAULT_TIMEOUT = 60


class SkopeoAnalyzer(BaseAnalyzer):
    """Fetch metadata for a Docker image using skopeo. Provides raw inspect data and structured platform details."""

    name = "skopeo"
    schema_file = "skopeo.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        """Return a report with raw skopeo inspect data and per-platform metadata."""
        # 'registry-1.docker.io' -> 'docker.io' for skopeo compatibility
        registry = client.registry
        if registry == "registry-1.docker.io":
            registry = "docker.io"

        target = f"docker://{registry}/{repository}:{tag}"

        # 1. Fetch raw manifest (to see if it's an index)
        try:
            raw_manifest_stdout = self._run_skopeo(client, ["inspect", "--raw", target])
            manifest = json.loads(raw_manifest_stdout)
        except subprocess.CalledProcessError as e:
            msg = f"Skopeo inspect --raw failed for {target}: {e.stderr}"
            logger.error(msg)
            raise AnalyzerError(msg) from e
        except Exception as e:
            msg = f"Failed to fetch raw manifest for {target}: {e}"
            logger.error(msg)
            raise AnalyzerError(msg) from e

        # 2. Resolve platforms
        media_type = manifest.get("mediaType", "")
        platforms: list[dict[str, Any]] = []

        # 3. Fetch primary inspect data (raw metadata) if NOT an index.
        # Calling high-level inspect on an index from a machine with different architecture
        # (e.g. arm64 local vs amd64 remote) often fails with 'no image found'.
        inspect_data: dict[str, Any] = {}
        if media_type not in _INDEX_TYPES:
            try:
                primary_inspect_stdout = self._run_skopeo(client, ["inspect", target])
                inspect_data = json.loads(primary_inspect_stdout)
            except Exception as e:
                logger.warning(
                    "Could not fetch primary inspect data for %s: %s", target, e
                )

        if media_type in _INDEX_TYPES:
            # Multi-arch image — iterate over each platform manifest in parallel.
            entries = manifest.get("manifests", [])
            # Limit workers to avoid overwhelming the system
            max_workers = min(10, len(entries) or 1)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for entry in entries:
                    platform_info = entry.get("platform", {})
                    digest = entry.get("digest", "")
                    futures.append(
                        executor.submit(
                            self._inspect_platform,
                            client,
                            registry,
                            repository,
                            digest,
                            platform_info,
                        )
                    )
                for future in futures:
                    try:
                        platforms.append(future.result())
                    except Exception as e:
                        logger.error("Failed to inspect platform: %s", e)
        else:
            # Single-platform manifest or fallback.
            detail = self._inspect_platform(client, registry, repository, tag, {})
            # If we already have the raw manifest with layers, use it.
            if "layers" in manifest:
                detail["layers_count"] = len(manifest["layers"])
            platforms.append(detail)

        # 4. List tags
        tags: list[str] = []
        try:
            # skopeo list-tags docker://registry/repository
            list_tags_target = f"docker://{registry}/{repository}"
            list_tags_stdout = self._run_skopeo(client, ["list-tags", list_tags_target])
            tags_data = json.loads(list_tags_stdout)
            tags = tags_data.get("Tags", [])
            # Natural sort or just take the ones from skopeo (usually unsorted or alphabetical)
            # We'll return the raw list and let the renderer handle it, but we can also store a subset.
        except Exception as e:
            logger.warning("Could not list tags for %s: %s", repository, e)

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "inspect": inspect_data,
            "platforms": platforms,
            "tags": tags,
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

        logger.debug("Running skopeo: %s", " ".join(cmd))
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=DEFAULT_TIMEOUT,
            )
            return res.stdout
        except subprocess.CalledProcessError as e:
            # Ensure we have stderr in the error message
            raise e from None
        except FileNotFoundError:
            raise AnalyzerError(
                "skopeo not found. Ensure it is installed and in PATH."
            ) from None

    def _inspect_platform(
        self,
        client: RegistryClient,
        registry: str,
        repository: str,
        ref: str,
        platform_info: dict[str, Any],
    ) -> dict[str, Any]:
        """Inspect a single platform by running skopeo inspect."""
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

        # 1. Run high-level inspect to get Architecture, Os, Labels, Created, and Layers count.
        args = ["inspect"]
        if result["os"] != "unknown":
            args.extend(["--override-os", result["os"]])
        if result["architecture"] != "unknown":
            args.extend(["--override-arch", result["architecture"]])
        args.append(target)

        try:
            inspect_stdout = self._run_skopeo(client, args)
            data = json.loads(inspect_stdout)

            result["created"] = data.get("Created")
            result["labels"] = data.get("Labels") or {}
            result["layers_count"] = len(data.get("Layers", []))

            if result["architecture"] == "unknown":
                result["architecture"] = data.get("Architecture", "unknown")
            if result["os"] == "unknown":
                result["os"] = data.get("Os", "unknown")
            if "digest" not in result or not result["digest"]:
                result["digest"] = data.get("Digest")

        except subprocess.CalledProcessError as e:
            logger.debug("Skopeo command failed for %s: %s", target, e.stderr)
        except Exception:
            logger.debug("Could not inspect platform %s", target, exc_info=True)

        # 2. Run --config inspect to get the User field
        config_args = ["inspect", "--config"]
        if result["os"] != "unknown":
            config_args.extend(["--override-os", result["os"]])
        if result["architecture"] != "unknown":
            config_args.extend(["--override-arch", result["architecture"]])
        config_args.append(target)

        try:
            config_stdout = self._run_skopeo(client, config_args)
            config_data = json.loads(config_stdout)
            # The User field is usually in the 'config' section of the config blob
            result["user"] = config_data.get("config", {}).get("User", "")
        except Exception:
            logger.debug(
                "Could not fetch config for platform %s", target, exc_info=True
            )
            result["user"] = "unknown"

        return result
