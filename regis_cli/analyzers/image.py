"""Image analyzer — inspects metadata for a specific tag."""

from __future__ import annotations

import logging
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
    """Inspect image metadata for a given tag. Resolves multi-arch manifests and reports per-platform details including architecture, OS, creation date, labels and layer count."""

    name = "image"
    schema_file = "image.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        """Return a report with image metadata for *tag*."""
        manifest = client.get_manifest(tag)
        media_type = manifest.get("mediaType", "")

        platforms: list[dict[str, Any]] = []

        if media_type in _INDEX_TYPES:
            # Multi-arch image — iterate over each platform manifest.
            for entry in manifest.get("manifests", []):
                platform_info = entry.get("platform", {})
                digest = entry.get("digest", "")
                detail = self._inspect_platform(
                    client, digest, platform_info
                )
                platforms.append(detail)
        elif media_type in _MANIFEST_TYPES:
            # Single-platform manifest.
            detail = self._inspect_single(client, manifest)
            platforms.append(detail)
        else:
            # Best-effort fallback for unknown media types.
            logger.warning("Unknown manifest mediaType: %s", media_type)
            detail = self._inspect_single(client, manifest)
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
    def _inspect_platform(
        client: RegistryClient,
        digest: str,
        platform_info: dict[str, Any],
    ) -> dict[str, Any]:
        """Inspect a single platform within a manifest list."""
        result: dict[str, Any] = {
            "architecture": platform_info.get("architecture", "unknown"),
            "os": platform_info.get("os", "unknown"),
            "digest": digest,
        }
        if "variant" in platform_info:
            result["variant"] = platform_info["variant"]

        # Fetch the platform-specific manifest to get the config blob.
        try:
            plat_manifest = client.get_manifest(digest)
            config_digest = plat_manifest.get("config", {}).get("digest", "")
            if config_digest:
                config = client.get_blob(config_digest)
                result["created"] = config.get("created")
                result["labels"] = (
                    config.get("config", {}).get("Labels") or {}
                )
            result["layers_count"] = len(plat_manifest.get("layers", []))
        except Exception:
            logger.debug("Could not inspect platform %s", digest, exc_info=True)

        return result

    @staticmethod
    def _inspect_single(
        client: RegistryClient,
        manifest: dict[str, Any],
    ) -> dict[str, Any]:
        """Inspect a single-platform manifest."""
        result: dict[str, Any] = {
            "architecture": "unknown",
            "os": "unknown",
        }
        config_digest = manifest.get("config", {}).get("digest", "")
        if config_digest:
            try:
                config = client.get_blob(config_digest)
                result["architecture"] = config.get("architecture", "unknown")
                result["os"] = config.get("os", "unknown")
                result["created"] = config.get("created")
                result["labels"] = (
                    config.get("config", {}).get("Labels") or {}
                )
            except Exception:
                logger.debug("Could not fetch config blob", exc_info=True)

        result["layers_count"] = len(manifest.get("layers", []))
        return result
