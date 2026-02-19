"""Tests for the CLI."""

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
        result = runner.invoke(
            main, ["analyze", "nginx", "-a", "nonexistent"]
        )
        assert result.exit_code != 0
        assert "Unknown analyzer" in result.output
