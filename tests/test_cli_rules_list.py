"""Tests for 'regis-cli rules list' command."""

import json
from pathlib import Path

from click.testing import CliRunner

from regis_cli.cli import main


class TestCliRulesList:
    """Test 'rules list' command behavior."""

    def test_rules_list_text(self):
        """Test default text output."""
        runner = CliRunner()
        result = runner.invoke(main, ["rules", "list"])
        assert result.exit_code == 0
        assert "core-trusted-domain" in result.output
        assert "critical" in result.output
        assert "Image must originate from a trusted domain." in result.output

    def test_rules_list_markdown(self):
        """Test markdown output."""
        runner = CliRunner()
        result = runner.invoke(main, ["rules", "list", "--format", "markdown"])
        assert result.exit_code == 0
        assert (
            "| Provider | Slug | Description | Level | Tags | Parameters |"
            in result.output
        )
        assert (
            "| core | `core-trusted-domain` | Image must originate from a trusted domain. | critical | security | `domains=['docker.io', 'registry-1.docker.io', 'quay.io', 'ghcr.io']` |"
            in result.output
        )

    def test_rules_list_output_file(self):
        """Test writing to a file."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            output_file = "rules.md"
            result = runner.invoke(
                main, ["rules", "list", "--format", "markdown", "--output", output_file]
            )
            assert result.exit_code == 0
            assert f"Rules list written to {output_file}" in result.output

            content = Path(output_file).read_text(encoding="utf-8")
            assert "| Provider |" in content
            assert "| `core-trusted-domain` |" in content

    def test_rules_list_markdown_output_dir(self):
        """Test multi-file markdown output."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            output_dir = "rules_doc"
            result = runner.invoke(
                main,
                [
                    "rules",
                    "list",
                    "--format",
                    "markdown",
                    "--output-dir",
                    output_dir,
                    "--index",
                ],
            )
            assert result.exit_code == 0
            assert f"rule files written to {output_dir}" in result.output
            assert f"Index file written to {output_dir}/index.md" in result.output

            out_path = Path(output_dir)
            assert (out_path / "index.md").exists()
            assert (out_path / "core-trusted-domain.md").exists()

            index_content = (out_path / "index.md").read_text(encoding="utf-8")
            assert "| Provider |" in index_content
            assert "[`core-trusted-domain`](./core-trusted-domain.md)" in index_content

            rule_content = (out_path / "core-trusted-domain.md").read_text(
                encoding="utf-8"
            )
            assert "# core-trusted-domain" in rule_content
            assert (
                "**Description**: Image must originate from a trusted domain."
                in rule_content
            )
            assert "**Provider**: core" in rule_content
            assert "## Condition" in rule_content
