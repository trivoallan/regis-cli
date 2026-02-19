"""Tests for the analyzers — uses mocked registry data."""

import json

import jsonschema
import pytest

from regis_cli.analyzers.image import ImageAnalyzer
from regis_cli.analyzers.tags import TagsAnalyzer

# ---------------------------------------------------------------------------
# Fixtures — mock RegistryClient
# ---------------------------------------------------------------------------


class MockRegistryClient:
    """Minimal mock for RegistryClient."""

    def __init__(self, tags=None, manifest=None, blobs=None):
        self._tags = tags or []
        self._manifest = manifest or {}
        self._blobs = blobs or {}

    def list_tags(self):
        return sorted(self._tags)

    def get_manifest(self, tag):
        if tag.startswith("sha256:"):
            return self._blobs.get(f"manifest:{tag}", self._manifest)
        return self._manifest

    def get_blob(self, digest):
        return self._blobs.get(digest, {})


# ---------------------------------------------------------------------------
# TagsAnalyzer
# ---------------------------------------------------------------------------


class TestTagsAnalyzer:
    """Test the tags analyzer."""

    def test_produces_valid_report(self):
        client = MockRegistryClient(tags=["latest", "1.0", "2.0", "alpine"])
        analyzer = TagsAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")

        # Should not raise.
        analyzer.validate(report)

        assert report["analyzer"] == "tags"
        assert report["repository"] == "library/nginx"
        assert report["count"] == 4
        assert "alpine" in report["tags"]

    def test_empty_tags(self):
        client = MockRegistryClient(tags=[])
        analyzer = TagsAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")
        analyzer.validate(report)
        assert report["count"] == 0
        assert report["tags"] == []


# ---------------------------------------------------------------------------
# ImageAnalyzer
# ---------------------------------------------------------------------------


class TestImageAnalyzer:
    """Test the image analyzer."""

    def test_single_platform_manifest(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:abc123"},
            "layers": [{"digest": "sha256:layer1"}, {"digest": "sha256:layer2"}],
        }
        config_blob = {
            "architecture": "amd64",
            "os": "linux",
            "created": "2024-01-15T10:00:00Z",
            "config": {"Labels": {"maintainer": "test"}},
        }
        client = MockRegistryClient(
            manifest=manifest,
            blobs={"sha256:abc123": config_blob},
        )

        analyzer = ImageAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")
        analyzer.validate(report)

        assert report["analyzer"] == "image"
        assert report["repository"] == "library/nginx"
        assert report["tag"] == "latest"
        assert len(report["platforms"]) == 1

        plat = report["platforms"][0]
        assert plat["architecture"] == "amd64"
        assert plat["os"] == "linux"
        assert plat["layers_count"] == 2

    def test_multi_arch_manifest(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
            "manifests": [
                {
                    "digest": "sha256:amd64digest",
                    "platform": {"architecture": "amd64", "os": "linux"},
                },
                {
                    "digest": "sha256:arm64digest",
                    "platform": {"architecture": "arm64", "os": "linux", "variant": "v8"},
                },
            ],
        }
        amd64_manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:amd64config"},
            "layers": [{"digest": "sha256:l1"}],
        }
        arm64_manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:arm64config"},
            "layers": [{"digest": "sha256:l1"}, {"digest": "sha256:l2"}],
        }
        blobs = {
            "manifest:sha256:amd64digest": amd64_manifest,
            "manifest:sha256:arm64digest": arm64_manifest,
            "sha256:amd64config": {
                "architecture": "amd64",
                "os": "linux",
                "created": "2024-01-15T10:00:00Z",
                "config": {"Labels": {}},
            },
            "sha256:arm64config": {
                "architecture": "arm64",
                "os": "linux",
                "created": "2024-01-15T11:00:00Z",
                "config": {"Labels": {}},
            },
        }
        client = MockRegistryClient(manifest=manifest, blobs=blobs)

        analyzer = ImageAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")
        analyzer.validate(report)

        assert len(report["platforms"]) == 2
        archs = {p["architecture"] for p in report["platforms"]}
        assert archs == {"amd64", "arm64"}


# ---------------------------------------------------------------------------
# Schema validation — negative tests
# ---------------------------------------------------------------------------


class TestSchemaValidation:
    """Verify that invalid reports are rejected by schema validation."""

    def test_tags_report_missing_field(self):
        analyzer = TagsAnalyzer()
        bad_report = {"analyzer": "tags", "repository": "test"}
        with pytest.raises(Exception):
            analyzer.validate(bad_report)

    def test_image_report_wrong_analyzer_name(self):
        analyzer = ImageAnalyzer()
        bad_report = {
            "analyzer": "wrong",
            "repository": "test",
            "tag": "latest",
            "platforms": [],
        }
        with pytest.raises(Exception):
            analyzer.validate(bad_report)
