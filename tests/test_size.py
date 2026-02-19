"""Tests for the size analyzer."""

from regis_cli.analyzers.size import SizeAnalyzer, _human_size


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


class TestHumanSize:
    def test_bytes(self):
        assert _human_size(500) == "500.0 B"

    def test_kb(self):
        assert _human_size(2048) == "2.0 KB"

    def test_mb(self):
        assert _human_size(5 * 1024 * 1024) == "5.0 MB"


class TestSizeAnalyzer:
    def test_single_manifest(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:cfg1", "size": 1500},
            "layers": [
                {"size": 10000, "digest": "sha256:l1"},
                {"size": 20000, "digest": "sha256:l2"},
            ],
        }
        client = MockRegistryClient(manifest=manifest)
        analyzer = SizeAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")
        analyzer.validate(report)

        assert report["multi_arch"] is False
        assert report["total_compressed_bytes"] == 31500
        assert report["layer_count"] == 2
        assert len(report["layers"]) == 2

    def test_empty_manifest(self):
        client = MockRegistryClient(manifest={})
        analyzer = SizeAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")
        analyzer.validate(report)

        assert report["layer_count"] == 0
