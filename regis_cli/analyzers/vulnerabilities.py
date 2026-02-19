"""Vulnerabilities analyzer — queries OSV.dev for known CVEs."""

from __future__ import annotations

import logging
from typing import Any

import requests

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)

_OSV_API = "https://api.osv.dev/v1/query"

# Map Docker image names to OSV ecosystem + package names where applicable.
_IMAGE_TO_ECOSYSTEM: dict[str, tuple[str, str]] = {
    "nginx": ("", "nginx"),
    "node": ("npm", "node"),
    "python": ("PyPI", "cpython"),
    "golang": ("Go", "stdlib"),
    "ruby": ("RubyGems", "ruby"),
    "php": ("Packagist", "php"),
    "postgres": ("", "postgresql"),
    "mysql": ("", "mysql"),
    "redis": ("", "redis"),
    "alpine": ("Alpine", "alpine"),
    "debian": ("Debian", "debian"),
    "ubuntu": ("Ubuntu", "ubuntu"),
}


def _extract_version(tag: str) -> str | None:
    """Extract a version string from a tag."""
    import re
    match = re.match(r"v?(\d+(?:\.\d+)*)", tag)
    return match.group(1) if match else None


def _query_osv(name: str, version: str, ecosystem: str = "") -> list[dict[str, Any]]:
    """Query OSV.dev for vulnerabilities affecting a package version."""
    payload: dict[str, Any] = {
        "package": {"name": name},
    }
    if ecosystem:
        payload["package"]["ecosystem"] = ecosystem
    if version:
        payload["version"] = version

    logger.debug("Querying OSV.dev: %s", payload)
    try:
        resp = requests.post(_OSV_API, json=payload, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("vulns", [])  # type: ignore[no-any-return]
        logger.info("OSV.dev returned %d", resp.status_code)
    except Exception:
        logger.debug("OSV.dev request failed", exc_info=True)
    return []


class VulnerabilitiesAnalyzer(BaseAnalyzer):
    """Check for known vulnerabilities via OSV.dev."""

    name = "vulnerabilities"
    schema_file = "vulnerabilities.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        # Map image to ecosystem/package.
        short_name = repository.removeprefix("library/").rsplit("/", 1)[-1]
        mapping = _IMAGE_TO_ECOSYSTEM.get(short_name)

        version = _extract_version(tag)

        if not mapping or not version:
            return {
                "analyzer": self.name,
                "repository": repository,
                "tag": tag,
                "package_name": short_name,
                "version_queried": version,
                "osv_available": False,
                "vulnerability_count": 0,
                "vulnerabilities": [],
            }

        ecosystem, package_name = mapping
        raw_vulns = _query_osv(package_name, version, ecosystem)

        # Simplify vulnerability entries.
        vulns = []
        for v in raw_vulns:
            aliases = v.get("aliases", [])
            cve_ids = [a for a in aliases if a.startswith("CVE-")]
            severity = "unknown"
            for sev in v.get("severity", []):
                if sev.get("type") == "CVSS_V3":
                    severity = sev.get("score", "unknown")
                    break
            for db_sev in v.get("database_specific", {}).get("severity", []):
                if isinstance(db_sev, str):
                    severity = db_sev
                    break

            vulns.append({
                "id": v.get("id", ""),
                "summary": v.get("summary", "")[:200],
                "cve_ids": cve_ids,
                "severity": severity,
                "published": v.get("published"),
                "modified": v.get("modified"),
            })

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "package_name": package_name,
            "version_queried": version,
            "osv_available": True,
            "vulnerability_count": len(vulns),
            "vulnerabilities": vulns,
        }
