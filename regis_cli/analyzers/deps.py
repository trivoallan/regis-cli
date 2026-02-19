"""Deps analyzer — detects base images from history and checks their EOL status."""

from __future__ import annotations

import logging
import re
from typing import Any

import requests

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.analyzers.endoflife import _fetch_cycles, _image_to_product, _extract_version, _match_cycle
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)

# Regex to detect FROM instructions in image history.
_FROM_RE = re.compile(
    r"(?:^|\s)FROM\s+(?P<image>[a-zA-Z0-9._/-]+?)(?::(?P<tag>[a-zA-Z0-9._-]+))?\s",
    re.IGNORECASE,
)

# Common base image prefixes to look for in history created_by.
_BASE_IMAGE_LABELS = (
    "org.opencontainers.image.base.name",
    "org.opencontainers.image.base.digest",
)


def _detect_base_images(config: dict[str, Any]) -> list[dict[str, str | None]]:
    """Detect base images from the image config history and labels.

    Returns a list of dicts with keys: ``image``, ``tag``, ``digest``.
    """
    bases: list[dict[str, str | None]] = []
    seen: set[str] = set()

    # Method 1: Check OCI base image labels.
    labels = config.get("config", {}).get("Labels") or {}
    base_name = labels.get("org.opencontainers.image.base.name")
    base_digest = labels.get("org.opencontainers.image.base.digest")
    if base_name:
        # base_name can be "docker.io/library/alpine:3.19"
        parts = base_name.rsplit(":", 1)
        image = parts[0].split("/")[-1] if "/" in parts[0] else parts[0]
        # Also keep the full reference for context.
        full_image = parts[0]
        tag = parts[1] if len(parts) > 1 else None
        key = f"{full_image}:{tag}"
        if key not in seen:
            seen.add(key)
            bases.append({
                "image": full_image,
                "tag": tag,
                "digest": base_digest,
            })

    # Method 2: Parse history entries for FROM instructions.
    for entry in config.get("history", []):
        created_by = entry.get("created_by", "")
        # Docker buildkit uses #(nop) markers or direct FROM.
        match = _FROM_RE.search(created_by)
        if match:
            image = match.group("image")
            tag = match.group("tag")
            if image.lower() in ("scratch",):
                continue
            key = f"{image}:{tag}"
            if key not in seen:
                seen.add(key)
                bases.append({"image": image, "tag": tag, "digest": None})

    return bases


def _check_eol(image: str, tag: str | None) -> dict[str, Any]:
    """Check end-of-life status for a base image."""
    # Extract the short name for endoflife.date lookup.
    short_name = image.rsplit("/", 1)[-1] if "/" in image else image
    product = _image_to_product(f"library/{short_name}")

    cycles = _fetch_cycles(product)
    if cycles is None:
        return {"product": product, "product_found": False, "is_eol": None, "cycle": None}

    version = _extract_version(tag) if tag else None
    matched = _match_cycle(version, cycles) if version else None

    is_eol: bool | None = None
    cycle_id: str | None = None
    if matched:
        cycle_id = str(matched.get("cycle", ""))
        eol_value = matched.get("eol")
        if eol_value is False:
            is_eol = False
        elif isinstance(eol_value, str):
            is_eol = True
        else:
            is_eol = bool(eol_value)

    return {
        "product": product,
        "product_found": True,
        "is_eol": is_eol,
        "cycle": cycle_id,
    }


class DepsAnalyzer(BaseAnalyzer):
    """Detect base images (FROM) and check their end-of-life status."""

    name = "deps"
    schema_file = "deps.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        config: dict[str, Any] = {}

        try:
            manifest = client.get_manifest(tag)
            media_type = manifest.get("mediaType", "")
            if "list" in media_type or "index" in media_type:
                entries = manifest.get("manifests", [])
                if entries:
                    manifest = client.get_manifest(entries[0]["digest"])

            config_digest = manifest.get("config", {}).get("digest")
            if config_digest:
                config = client.get_blob(config_digest)
        except Exception:
            logger.debug("Could not fetch image config for deps", exc_info=True)

        raw_bases = _detect_base_images(config)

        dependencies: list[dict[str, Any]] = []
        any_eol = False

        for base in raw_bases:
            eol_info = _check_eol(base["image"], base["tag"])
            dep = {
                "image": base["image"],
                "tag": base["tag"],
                "digest": base["digest"],
                "eol_check": eol_info,
            }
            dependencies.append(dep)
            if eol_info["is_eol"] is True:
                any_eol = True

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "base_image_count": len(dependencies),
            "has_eol_dependency": any_eol,
            "dependencies": dependencies,
        }
