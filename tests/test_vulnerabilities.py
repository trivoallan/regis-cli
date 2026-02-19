"""Tests for the vulnerabilities analyzer."""

from regis_cli.analyzers.vulnerabilities import VulnerabilitiesAnalyzer


class MockRegistryClient:
    def list_tags(self):
        return []

    def get_manifest(self, tag):
        return {}

    def get_blob(self, digest):
        return {}


class TestVulnerabilitiesAnalyzer:
    def test_unknown_image(self):
        client = MockRegistryClient()
        analyzer = VulnerabilitiesAnalyzer()
        report = analyzer.analyze(client, "fakens/myapp", "latest")
        analyzer.validate(report)

        assert report["osv_available"] is False
        assert report["vulnerability_count"] == 0

    def test_no_version_tag(self):
        client = MockRegistryClient()
        analyzer = VulnerabilitiesAnalyzer()
        report = analyzer.analyze(client, "library/nginx", "alpine")
        analyzer.validate(report)

        assert report["osv_available"] is False
