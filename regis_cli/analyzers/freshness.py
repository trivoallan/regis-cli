"""Freshness analyzer — checks how up-to-date the image tag is."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)


def _get_created_date(client: RegistryClient, tag_or_digest: str) -> str | None:
    """Extract the creation date from an image config."""
    try:
        manifest = client.get_manifest(tag_or_digest)
        media_type = manifest.get("mediaType", "")
        if "list" in media_type or "index" in media_type:
            entries = manifest.get("manifests", [])
            if not entries:
                return None
            manifest = client.get_manifest(entries[0]["digest"])

        config_digest = manifest.get("config", {}).get("digest")
        if not config_digest:
            return None
        config = client.get_blob(config_digest)
        return config.get("created")  # type: ignore[no-any-return]
    except Exception:
        logger.debug("Could not fetch image config", exc_info=True)
        return None


class FreshnessAnalyzer(BaseAnalyzer):
    """Compare the analyzed tag's creation date against the latest tag."""

    name = "freshness"
    schema_file = "freshness.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        # Get creation date for the analyzed tag.
        tag_created = _get_created_date(client, tag)

        # Get creation date for "latest".
        latest_created = None
        if tag != "latest":
            latest_created = _get_created_date(client, "latest")

        # Compute age and delta.
        age_days: int | None = None
        behind_days: int | None = None
        now = datetime.now(timezone.utc)

        if tag_created:
            try:
                tag_dt = datetime.fromisoformat(tag_created.replace("Z", "+00:00"))
                age_days = (now - tag_dt).days
            except (ValueError, TypeError):
                pass

        if tag_created and latest_created:
            try:
                tag_dt = datetime.fromisoformat(tag_created.replace("Z", "+00:00"))
                latest_dt = datetime.fromisoformat(latest_created.replace("Z", "+00:00"))
                behind_days = (latest_dt - tag_dt).days
                if behind_days < 0:
                    behind_days = 0
            except (ValueError, TypeError):
                pass

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "tag_created": tag_created,
            "latest_created": latest_created,
            "age_days": age_days,
            "behind_latest_days": behind_days,
            "is_latest": tag == "latest" or behind_days == 0,
        }
