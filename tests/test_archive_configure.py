"""Tests for regis archive configure command."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from regis.cli import main


class TestArchiveConfigureAdd:
    """Tests for non-interactive --add mode."""

    def test_add_creates_new_config(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "archive",
                "configure",
                "-o",
                str(out),
                "--add",
                "Prod:static/archive/prod",
            ],
        )
        assert result.exit_code == 0, result.output
        data = json.loads(out.read_text())
        assert len(data["archives"]) == 1
        assert data["archives"][0] == {"name": "Prod", "path": "static/archive/prod"}

    def test_add_appends_to_existing(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        out.write_text(json.dumps({"archives": [{"name": "Prod", "path": "p"}]}))
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "archive",
                "configure",
                "-o",
                str(out),
                "--add",
                "Staging:static/archive/staging",
            ],
        )
        assert result.exit_code == 0, result.output
        data = json.loads(out.read_text())
        assert len(data["archives"]) == 2

    def test_add_rejects_duplicate_name(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        out.write_text(json.dumps({"archives": [{"name": "Prod", "path": "p"}]}))
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["archive", "configure", "-o", str(out), "--add", "Prod:other/path"],
        )
        assert result.exit_code != 0
        assert "already exists" in result.output.lower()

    def test_add_rejects_invalid_format(self) -> None:
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["archive", "configure", "--add", "no-colon-here"],
        )
        assert result.exit_code != 0
        assert "invalid format" in result.output.lower()

    def test_add_rejects_empty_name(self) -> None:
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["archive", "configure", "--add", ":some/path"],
        )
        assert result.exit_code != 0
        assert "must not be empty" in result.output.lower()

    def test_add_url_with_port(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "archive",
                "configure",
                "-o",
                str(out),
                "--add",
                "Remote:https://host:8080/archive/manifest.json",
            ],
        )
        assert result.exit_code == 0, result.output
        data = json.loads(out.read_text())
        assert data["archives"][0]["path"] == "https://host:8080/archive/manifest.json"


class TestArchiveConfigureList:
    """Tests for --list mode."""

    def test_list_empty(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        runner = CliRunner()
        result = runner.invoke(main, ["archive", "configure", "-o", str(out), "--list"])
        assert result.exit_code == 0
        assert "no archives" in result.output.lower()

    def test_list_shows_archives(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        out.write_text(
            json.dumps(
                {
                    "archives": [
                        {"name": "Prod", "path": "prod/"},
                        {"name": "Staging", "path": "staging/"},
                    ]
                }
            )
        )
        runner = CliRunner()
        result = runner.invoke(main, ["archive", "configure", "-o", str(out), "--list"])
        assert result.exit_code == 0
        assert "Prod" in result.output
        assert "Staging" in result.output


class TestArchiveConfigureRemove:
    """Tests for --remove mode."""

    def test_remove_existing(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        out.write_text(
            json.dumps(
                {
                    "archives": [
                        {"name": "Prod", "path": "p"},
                        {"name": "Staging", "path": "s"},
                    ]
                }
            )
        )
        runner = CliRunner()
        result = runner.invoke(
            main, ["archive", "configure", "-o", str(out), "--remove", "Prod"]
        )
        assert result.exit_code == 0, result.output
        data = json.loads(out.read_text())
        assert len(data["archives"]) == 1
        assert data["archives"][0]["name"] == "Staging"

    def test_remove_nonexistent_fails(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        out.write_text(json.dumps({"archives": [{"name": "Prod", "path": "p"}]}))
        runner = CliRunner()
        result = runner.invoke(
            main, ["archive", "configure", "-o", str(out), "--remove", "Nope"]
        )
        assert result.exit_code != 0
        assert "not found" in result.output.lower()


class TestArchiveConfigureInteractive:
    """Tests for interactive mode."""

    def test_interactive_add_two(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["archive", "configure", "-o", str(out)],
            input="Prod\nstatic/archive/prod\nStaging\nstatic/archive/staging\n\n",
        )
        assert result.exit_code == 0, result.output
        data = json.loads(out.read_text())
        assert len(data["archives"]) == 2

    def test_interactive_empty_exits(self, tmp_path: Path) -> None:
        out = tmp_path / "archives.json"
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["archive", "configure", "-o", str(out)],
            input="\n",
        )
        assert result.exit_code == 0
        assert not out.exists()


class TestArchiveConfigureHelp:
    def test_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["archive", "configure", "--help"])
        assert result.exit_code == 0
        assert "--add" in result.output
        assert "--list" in result.output
        assert "--remove" in result.output
