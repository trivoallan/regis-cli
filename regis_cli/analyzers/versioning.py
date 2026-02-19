"""Versioning analyzer — detects tag naming patterns (semver, calver, etc.)."""

from __future__ import annotations

import re
from typing import Any

import semver

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.registry.client import RegistryClient

# ---------------------------------------------------------------------------
# Pattern classifiers — order matters (first match wins for each tag).
# ---------------------------------------------------------------------------

# CalVer patterns like 2024.01, 2024.01.15, 20240115
_CALVER_RE = re.compile(
    r"^v?(?:20\d{2})(?:[.\-](?:0[1-9]|1[0-2]))(?:[.\-](?:0[1-9]|[12]\d|3[01]))?$"
)

# Loose numeric versions like 1, 1.2, 1.2.3.4 (not strict semver)
_NUMERIC_RE = re.compile(r"^v?\d+(?:\.\d+)*$")

# Hash-like tags (hex strings ≥ 7 chars)
_HASH_RE = re.compile(r"^[0-9a-f]{7,}$")

# Known OS / distro variant tokens.  When all parts of a semver "prerelease"
# string consist of these tokens, the tag is classified as ``semver-variant``
# rather than ``semver-prerelease``.
_VARIANT_TOKENS: set[str] = {
    # Debian / Ubuntu code-names
    "alpine", "bookworm", "bullseye", "buster", "focal", "jammy", "jessie",
    "noble", "stretch", "trixie", "trusty", "xenial",
    # Generic qualifiers
    "slim", "fat", "full", "minimal", "lite",
    # Explicit OS names
    "linux", "windows", "windowsservercore",
}

# Regex that matches alpine3.20, alpine3.21, etc. as a single variant token.
_VARIANT_TOKEN_RE = re.compile(r"^(" + "|".join(re.escape(t) for t in _VARIANT_TOKENS) + r")(\d[\w.]*)?$")

# Semver + variant pattern:  1.88.0-slim-bookworm, v2.0.0-alpine3.21
# Captures (optional v prefix)(semver digits)-(variant suffix)
_SEMVER_VARIANT_RE = re.compile(
    r"^v?(\d+\.\d+\.\d+)-(.+)$"
)


def _is_variant_suffix(suffix: str) -> bool:
    """Return True if *suffix* looks like an OS/distro variant, not a prerelease."""
    parts = suffix.split("-")
    return all(_VARIANT_TOKEN_RE.match(p) for p in parts)


def _classify_tag(tag: str) -> str:
    """Classify a single tag into a versioning pattern.

    Returns one of: ``semver``, ``semver-prerelease``, ``semver-variant``,
    ``calver``, ``numeric``, ``hash``, ``named``.
    """
    # Calendar versioning checked first — dates like 2024.12.25 are valid
    # semver too, but calver is the more specific classification.
    if _CALVER_RE.match(tag):
        return "calver"

    # Try strict semver.
    try:
        ver = semver.Version.parse(tag.lstrip("v"))
        if ver.prerelease:
            # Check whether the "prerelease" part is actually an OS variant.
            if _is_variant_suffix(ver.prerelease):
                return "semver-variant"
            return "semver-prerelease"
        return "semver"
    except ValueError:
        pass

    # Loose numeric (e.g. "1.2" or "8").
    if _NUMERIC_RE.match(tag):
        return "numeric"

    # Git commit hashes.
    if _HASH_RE.match(tag):
        return "hash"

    # Everything else is a named tag (latest, alpine, bookworm, …).
    return "named"


class VersioningAnalyzer(BaseAnalyzer):
    """Detect tag naming conventions and identify semver adoption."""

    name = "versioning"
    schema_file = "versioning.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        """Classify all tags and summarize versioning patterns."""
        tags = client.list_tags()

        # Classify every tag.
        classifications: dict[str, list[str]] = {}
        for t in tags:
            pattern = _classify_tag(t)
            classifications.setdefault(pattern, []).append(t)

        # Sort each bucket and compute stats.
        patterns: list[dict[str, Any]] = []
        for pattern_name in sorted(classifications):
            tag_list = sorted(classifications[pattern_name])
            patterns.append({
                "pattern": pattern_name,
                "count": len(tag_list),
                "percentage": round(len(tag_list) / len(tags) * 100, 1) if tags else 0,
                "examples": tag_list[:10],
            })

        # Determine the dominant pattern.
        dominant = max(patterns, key=lambda p: p["count"])["pattern"] if patterns else "unknown"

        # SemVer-specific summary (semver + prerelease + variant all count).
        semver_count = (
            len(classifications.get("semver", []))
            + len(classifications.get("semver-prerelease", []))
            + len(classifications.get("semver-variant", []))
        )
        semver_compliant = round(semver_count / len(tags) * 100, 1) if tags else 0

        return {
            "analyzer": self.name,
            "repository": repository,
            "total_tags": len(tags),
            "dominant_pattern": dominant,
            "semver_compliant_percentage": semver_compliant,
            "patterns": patterns,
        }
