"""Tests for the freshness analyzer."""

from regis_cli.analyzers.freshness import FreshnessAnalyzer


class MockRegistryClient:
    def __init__(self, manifest=None, blobs=None):
        self._manifest = manifest or {}
        self._blobs = blobs or {}

    def list_tags(self):
        return []

    def get_manifest(self, tag):
        if tag.startswith("sha256:"):
            return self._blobs.get(f"manifest:{tag}", self._manifest)
        return self._manifest

    def get_blob(self, digest):
        return self._blobs.get(digest, {})


class TestFreshnessAnalyzer:
    def test_with_created_date(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:cfg1"},
        }
        config = {
            "created": "2025-01-01T00:00:00Z",
            "config": {"Labels": {}},
        }
        client = MockRegistryClient(manifest=manifest, blobs={"sha256:cfg1": config})
        analyzer = FreshnessAnalyzer()
        report = analyzer.analyze(client, "library/test", "latest")
        analyzer.validate(report)

        assert report["tag_created"] == "2025-01-01T00:00:00Z"
        assert report["age_days"] is not None
        assert report["age_days"] > 0
        assert report["is_latest"] is True
