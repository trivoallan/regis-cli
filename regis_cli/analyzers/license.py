"""License analyzer — extracts license info from image labels or source repo."""

from __future__ import annotations

import logging
import re
from typing import Any

import requests

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)

_GIT_REPO_RE = re.compile(
    r"(?:https?://)?(?P<platform>github\.com|gitlab\.com)/(?P<owner>[a-zA-Z0-9._-]+)/(?P<repo>[a-zA-Z0-9._-]+)"
)


def _license_from_labels(labels: dict[str, str]) -> dict[str, str | None]:
    """Extract license information from OCI / label-schema labels."""
    result: dict[str, str | None] = {"spdx": None, "url": None, "source": None}

    for key in ("org.opencontainers.image.licenses", "license"):
        val = labels.get(key, "")
        if val:
            result["spdx"] = val
            result["source"] = "image-label"
            break

    url = labels.get("org.opencontainers.image.source", "")
    if url:
        result["url"] = url

    return result


def _license_from_github(owner: str, repo: str) -> dict[str, str | None]:
    """Fetch license from the GitHub API."""
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/license",
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            lic = data.get("license", {})
            return {
                "spdx": lic.get("spdx_id"),
                "url": data.get("html_url"),
                "source": "github-api",
            }
    except Exception:
        logger.debug("GitHub license API failed", exc_info=True)
    return {"spdx": None, "url": None, "source": None}


class LicenseAnalyzer(BaseAnalyzer):
    """Detect the license of the image or its source project."""

    name = "license"
    schema_file = "license.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        labels: dict[str, str] = {}

        # Try to get labels from the image config.
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
                labels = config.get("config", {}).get("Labels") or {}
        except Exception:
            logger.debug("Could not fetch image config for license", exc_info=True)

        # Try labels first.
        info = _license_from_labels(labels)

        # If no license in labels, try GitHub API using the source URL.
        if not info["spdx"]:
            source_url = labels.get("org.opencontainers.image.source", "")
            match = _GIT_REPO_RE.search(source_url)
            if match and match.group("platform") == "github.com":
                repo_name = match.group("repo")
                if repo_name.endswith(".git"):
                    repo_name = repo_name[:-4]
                info = _license_from_github(match.group("owner"), repo_name)

        return {
            "analyzer": self.name,
            "repository": repository,
            "spdx_id": info["spdx"],
            "license_url": info["url"],
            "detection_source": info["source"],
        }
