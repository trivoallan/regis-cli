"""Tests for the analyzers — uses mocked registry data."""

import json
from unittest.mock import patch

import pytest

from regis_cli.analyzers.base import AnalyzerError
from regis_cli.analyzers.skopeo import SkopeoAnalyzer
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
# Schema validation — negative tests
# ---------------------------------------------------------------------------


class TestSchemaValidation:
    """Verify that invalid reports are rejected by schema validation."""

    def test_tags_report_missing_field(self):
        analyzer = TagsAnalyzer()
        bad_report = {"analyzer": "tags", "repository": "test"}
        with pytest.raises(AnalyzerError):
            analyzer.validate(bad_report)

    def test_skopeo_report_wrong_analyzer_name(self):
        analyzer = SkopeoAnalyzer()
        bad_report = {
            "analyzer": "wrong",
            "repository": "test",
            "tag": "latest",
            "platforms": [],
        }
        with pytest.raises(AnalyzerError):
            analyzer.validate(bad_report)
