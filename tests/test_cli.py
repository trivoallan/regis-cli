"""Tests for the CLI."""

from unittest.mock import patch

from click.testing import CliRunner

from regis_cli.cli import main


class TestCliBasics:
    """Test basic CLI behavior."""

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "regis-cli" in result.output

    def test_analyze_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "URL" in result.output

    def test_list_command(self):
        runner = CliRunner()
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        # The built-in analyzers should appear.
        assert "tags" in result.output
        assert "image" in result.output

    def test_analyze_invalid_url(self):
        runner = CliRunner()
        result = runner.invoke(main, ["analyze", "https://myregistry.example.com/"])
        assert result.exit_code != 0

    def test_analyze_unknown_analyzer(self):
        runner = CliRunner()
        result = runner.invoke(main, ["analyze", "nginx", "-a", "nonexistent"])
        assert result.exit_code != 0
        assert "Unknown analyzer" in result.output

    @patch("regis_cli.cli.RegistryClient")
    @patch("regis_cli.cli._discover_analyzers")
    def test_analyze_with_metadata(self, mock_discover, mock_client):
        from regis_cli.analyzers.base import BaseAnalyzer

        class DummyAnalyzer(BaseAnalyzer):
            def analyze(self, client, repo, tag):
                return {"analyzer": "dummy", "repository": repo, "tag": tag}

            def validate(self, report):
                pass

        mock_discover.return_value = {"dummy": DummyAnalyzer}

        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "analyze",
                "nginx:latest",
                "--meta",
                "build=123",
                "--meta",
                "env=prod",
                "--meta",
                "flag_only",
            ],
        )
        assert result.exit_code == 0

        import json

        output = result.output
        json_str = output[output.find("{") :]
        report = json.loads(json_str)
        assert "metadata" in report
        assert report["metadata"]["build"] == "123"
        assert report["metadata"]["env"] == "prod"
        assert report["metadata"]["flag_only"] == "true"

    @patch("regis_cli.cli.RegistryClient")
    @patch("regis_cli.cli._discover_analyzers")
    def test_analyze_html_with_metadata(self, mock_discover, mock_client):
        from regis_cli.analyzers.base import BaseAnalyzer

        class DummyAnalyzer(BaseAnalyzer):
            def analyze(self, client, repo, tag):
                return {"analyzer": "dummy", "repository": repo, "tag": tag}

            def validate(self, report):
                pass

        mock_discover.return_value = {"dummy": DummyAnalyzer}

        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "analyze",
                "nginx:latest",
                "--format",
                "html",
                "--meta",
                "build=123",
                "--meta",
                "env=prod",
            ],
        )
        assert result.exit_code == 0
        assert "Metadata" in result.output
        assert "build" in result.output
        assert "123" in result.output
        assert "env" in result.output
        assert "prod" in result.output
