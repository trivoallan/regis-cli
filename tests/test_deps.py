"""Tests for the deps analyzer."""

from regis_cli.analyzers.deps import DepsAnalyzer, _detect_base_images


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


class TestDetectBaseImages:
    def test_from_oci_labels(self):
        config = {
            "config": {
                "Labels": {
                    "org.opencontainers.image.base.name": "docker.io/library/alpine:3.19",
                    "org.opencontainers.image.base.digest": "sha256:abc123",
                }
            },
            "history": [],
        }
        bases = _detect_base_images(config)
        assert len(bases) == 1
        assert bases[0]["image"] == "docker.io/library/alpine"
        assert bases[0]["tag"] == "3.19"
        assert bases[0]["digest"] == "sha256:abc123"

    def test_from_history(self):
        config = {
            "config": {"Labels": {}},
            "history": [
                {"created_by": " FROM debian:bookworm-slim "},
                {"created_by": "/bin/sh -c apt-get update"},
            ],
        }
        bases = _detect_base_images(config)
        assert len(bases) == 1
        assert bases[0]["image"] == "debian"
        assert bases[0]["tag"] == "bookworm-slim"

    def test_empty_config(self):
        config = {"config": {"Labels": {}}, "history": []}
        bases = _detect_base_images(config)
        assert bases == []


class TestDepsAnalyzer:
    def test_with_base_label(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:cfg1"},
        }
        config = {
            "config": {
                "Labels": {
                    "org.opencontainers.image.base.name": "docker.io/library/debian:bookworm",
                }
            },
            "history": [],
        }
        client = MockRegistryClient(manifest=manifest, blobs={"sha256:cfg1": config})
        analyzer = DepsAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "latest")
        analyzer.validate(report)

        assert report["base_image_count"] == 1
        assert report["dependencies"][0]["tag"] == "bookworm"

    def test_no_base(self):
        manifest = {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {"digest": "sha256:cfg1"},
        }
        config = {"config": {"Labels": {}}, "history": []}
        client = MockRegistryClient(manifest=manifest, blobs={"sha256:cfg1": config})
        analyzer = DepsAnalyzer()
        report = analyzer.analyze(client, "library/scratch-app", "latest")
        analyzer.validate(report)

        assert report["base_image_count"] == 0
        assert report["has_eol_dependency"] is False
