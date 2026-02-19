"""Tests for the license analyzer."""

from regis_cli.analyzers.license import LicenseAnalyzer


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


class TestLicenseAnalyzer:
    def test_from_labels(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:cfg1"},
        }
        config = {
            "config": {
                "Labels": {
                    "org.opencontainers.image.licenses": "Apache-2.0",
                    "org.opencontainers.image.source": "https://github.com/test/repo",
                }
            },
        }
        client = MockRegistryClient(manifest=manifest, blobs={"sha256:cfg1": config})
        analyzer = LicenseAnalyzer()
        report = analyzer.analyze(client, "library/test", "latest")
        analyzer.validate(report)

        assert report["spdx_id"] == "Apache-2.0"
        assert report["detection_source"] == "image-label"

    def test_no_labels(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:cfg1"},
        }
        config = {"config": {"Labels": {}}}
        client = MockRegistryClient(manifest=manifest, blobs={"sha256:cfg1": config})
        analyzer = LicenseAnalyzer()
        report = analyzer.analyze(client, "fakens/noinfo", "latest")
        analyzer.validate(report)

        assert report["spdx_id"] is None
