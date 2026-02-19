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


    def test_osv_results(self, monkeypatch):
        """Test parsing of OSV results including osv_url."""
        import requests
        
        # Mock the OSV API response
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "vulns": [
                        {
                            "id": "GHSA-1234-5678",
                            "summary": "Test Vulnerability",
                            "severity": [
                                {
                                    "type": "CVSS_V3",
                                    "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
                                }
                            ],
                            "published": "2023-01-01T00:00:00Z",
                            "modified": "2023-01-02T00:00:00Z"
                        }
                    ]
                }

        monkeypatch.setattr(requests, "post", lambda *args, **kwargs: MockResponse())

        client = MockRegistryClient()
        analyzer = VulnerabilitiesAnalyzer()
        # "python" maps to PyPI/cpython in the analyzer
        report = analyzer.analyze(client, "library/python", "3.9.0")
        analyzer.validate(report)

        assert report["osv_available"] is True
        assert report["vulnerability_count"] == 1
        vuln = report["vulnerabilities"][0]
        assert vuln["id"] == "GHSA-1234-5678"
        assert vuln["osv_url"] == "https://osv.dev/vulnerability/GHSA-1234-5678"
