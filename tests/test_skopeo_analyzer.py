"""Tests for the skopeo raw analyzer."""

import json
from unittest.mock import patch

from regis_cli.analyzers.skopeo import SkopeoAnalyzer


class MockRegistryClient:
    def __init__(self):
        self.registry = "registry-1.docker.io"
        self.username = None
        self.password = None


class TestSkopeoAnalyzer:
    @patch("regis_cli.analyzers.skopeo.subprocess.run")
    def test_skopeo_inspect(self, mock_run):
        mock_data = {
            "Digest": "sha256:123",
            "Created": "2024-01-01T00:00:00Z",
            "DockerVersion": "20.10.7",
            "Architecture": "amd64",
            "Os": "linux",
        }
        mock_run.return_value.stdout = json.dumps(mock_data)
        
        client = MockRegistryClient()
        analyzer = SkopeoAnalyzer()
        report = analyzer.analyze(client, "library/test", "latest")
        analyzer.validate(report)

        assert report["analyzer"] == "skopeo"
        assert report["inspect"]["Digest"] == "sha256:123"
        assert report["inspect"]["Architecture"] == "amd64"
