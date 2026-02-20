"""Tests for the analyzers — uses mocked registry data."""

import json
from unittest.mock import patch

import pytest

from regis_cli.analyzers.base import AnalyzerError
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
        self.registry = "registry-1.docker.io"
        self.username = None
        self.password = None

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

    @patch("regis_cli.analyzers.tags.subprocess.run")
    def test_produces_valid_report(self, mock_run):
        mock_run.return_value.stdout = json.dumps(
            {"Repository": "library/nginx", "Tags": ["latest", "1.0", "2.0", "alpine"]}
        )
        client = MockRegistryClient()
        analyzer = TagsAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")

        # Should not raise.
        analyzer.validate(report)

        assert report["analyzer"] == "tags"
        assert report["repository"] == "library/nginx"
        assert report["count"] == 4
        assert "alpine" in report["tags"]

    @patch("regis_cli.analyzers.tags.subprocess.run")
    def test_empty_tags(self, mock_run):
        mock_run.return_value.stdout = json.dumps(
            {"Repository": "library/nginx", "Tags": []}
        )
        client = MockRegistryClient()
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

    @patch("regis_cli.analyzers.image.subprocess.run")
    def test_single_platform_manifest(self, mock_run):
        def side_effect(cmd, **kwargs):
            class MockResponse:
                def __init__(self, stdout):
                    self.stdout = stdout

            if "--raw" in cmd:
                return MockResponse(
                    json.dumps(
                        {
                            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
                            "layers": [{}, {}],
                        }
                    )
                )
            else:
                return MockResponse(
                    json.dumps(
                        {
                            "architecture": "amd64",
                            "os": "linux",
                            "created": "2024-01-15T10:00:00Z",
                            "config": {"Labels": {"maintainer": "test"}},
                        }
                    )
                )

        mock_run.side_effect = side_effect
        client = MockRegistryClient()  # Only needed for the interface, no data required

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

    @patch("regis_cli.analyzers.image.subprocess.run")
    def test_multi_arch_manifest(self, mock_run):
        def side_effect(cmd, **kwargs):
            class MockResponse:
                def __init__(self, stdout):
                    self.stdout = stdout

            target = cmd[-1]
            if "--raw" in cmd:
                if "sha256:amd64digest" in target:
                    return MockResponse(json.dumps({"layers": [{}]}))
                if "sha256:arm64digest" in target:
                    return MockResponse(json.dumps({"layers": [{}, {}]}))
                # Otherwise, return index
                return MockResponse(
                    json.dumps(
                        {
                            "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
                            "manifests": [
                                {
                                    "digest": "sha256:amd64digest",
                                    "platform": {
                                        "architecture": "amd64",
                                        "os": "linux",
                                    },
                                },
                                {
                                    "digest": "sha256:arm64digest",
                                    "platform": {
                                        "architecture": "arm64",
                                        "os": "linux",
                                        "variant": "v8",
                                    },
                                },
                            ],
                        }
                    )
                )
            else:
                if "sha256:amd64digest" in target:
                    return MockResponse(
                        json.dumps(
                            {
                                "architecture": "amd64",
                                "os": "linux",
                                "created": "2024-01-15T10:00:00Z",
                            }
                        )
                    )
                if "sha256:arm64digest" in target:
                    return MockResponse(
                        json.dumps(
                            {
                                "architecture": "arm64",
                                "os": "linux",
                                "created": "2024-01-15T11:00:00Z",
                            }
                        )
                    )
            return MockResponse("{}")

        mock_run.side_effect = side_effect
        client = MockRegistryClient()

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
        with pytest.raises(AnalyzerError):
            analyzer.validate(bad_report)

    def test_image_report_wrong_analyzer_name(self):
        analyzer = ImageAnalyzer()
        bad_report = {
            "analyzer": "wrong",
            "repository": "test",
            "tag": "latest",
            "platforms": [],
        }
        with pytest.raises(AnalyzerError):
            analyzer.validate(bad_report)
