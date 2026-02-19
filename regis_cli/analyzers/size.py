"""Size analyzer — reports image size breakdown from manifest."""

from __future__ import annotations

import logging
from typing import Any

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)


def _human_size(size_bytes: int) -> str:
    """Convert bytes to human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024  # type: ignore[assignment]
    return f"{size_bytes:.1f} TB"


class SizeAnalyzer(BaseAnalyzer):
    """Analyze compressed image size from manifest layers."""

    name = "size"
    schema_file = "size.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        try:
            manifest = client.get_manifest(tag)
        except Exception:
            logger.debug("Could not fetch manifest", exc_info=True)
            return self._empty(repository, tag)

        media_type = manifest.get("mediaType", "")

        # Handle manifest list / OCI index.
        if "list" in media_type or "index" in media_type:
            return self._analyze_multiarch(client, repository, tag, manifest)

        return self._analyze_single(repository, tag, manifest)

    def _analyze_single(
        self,
        repository: str,
        tag: str,
        manifest: dict[str, Any],
    ) -> dict[str, Any]:
        layers = manifest.get("layers", [])
        config_size = manifest.get("config", {}).get("size", 0)

        layer_sizes = [layer.get("size", 0) for layer in layers]
        total_compressed = sum(layer_sizes) + config_size

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "multi_arch": False,
            "total_compressed_bytes": total_compressed,
            "total_compressed_human": _human_size(total_compressed),
            "layer_count": len(layers),
            "config_size_bytes": config_size,
            "layers": [
                {
                    "index": i,
                    "size_bytes": s,
                    "size_human": _human_size(s),
                }
                for i, s in enumerate(layer_sizes)
            ],
            "platforms": None,
        }

    def _analyze_multiarch(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
        manifest_list: dict[str, Any],
    ) -> dict[str, Any]:
        entries = manifest_list.get("manifests", [])
        platforms = []

        for entry in entries:
            platform = entry.get("platform", {})
            arch = platform.get("architecture", "unknown")
            os_name = platform.get("os", "unknown")
            variant = platform.get("variant", "")
            platform_label = f"{os_name}/{arch}"
            if variant:
                platform_label += f"/{variant}"

            # Fetch size for this platform.
            try:
                plat_manifest = client.get_manifest(entry["digest"])
                plat_layers = plat_manifest.get("layers", [])
                plat_config_size = plat_manifest.get("config", {}).get("size", 0)
                plat_layer_sizes = [l.get("size", 0) for l in plat_layers]
                plat_total = sum(plat_layer_sizes) + plat_config_size
            except Exception:
                plat_total = entry.get("size", 0)
                plat_layer_sizes = []
                plat_config_size = 0

            platforms.append({
                "platform": platform_label,
                "compressed_bytes": plat_total,
                "compressed_human": _human_size(plat_total),
                "layer_count": len(plat_layer_sizes),
            })

        # Use first platform as representative total.
        total = platforms[0]["compressed_bytes"] if platforms else 0

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "multi_arch": True,
            "total_compressed_bytes": total,
            "total_compressed_human": _human_size(total),
            "layer_count": platforms[0]["layer_count"] if platforms else 0,
            "config_size_bytes": 0,
            "layers": [],
            "platforms": platforms,
        }

    def _empty(self, repository: str, tag: str) -> dict[str, Any]:
        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "multi_arch": False,
            "total_compressed_bytes": 0,
            "total_compressed_human": "0.0 B",
            "layer_count": 0,
            "config_size_bytes": 0,
            "layers": [],
            "platforms": None,
        }
