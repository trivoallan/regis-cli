"""Tests for the regis-cli generate command."""

import os
from pathlib import Path

from click.testing import CliRunner

from regis_cli.cli import main


def test_generate_help():
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--help"])
    assert result.exit_code == 0
    assert "TEMPLATE_PATH" in result.output


def test_generate_github_success():
    runner = CliRunner()
    template_path = str(Path("cookiecutters/consumer").resolve())
    if not os.path.exists(template_path):
        template_path = str(Path("cookiecutters/project").resolve())

    with runner.isolated_filesystem():
        result = runner.invoke(
            main, ["generate", template_path, "test-output", "--no-input"]
        )

        assert result.exit_code == 0

        project_dir = Path("test-output/regis-image-security")
        assert project_dir.exists()
        assert (project_dir / "README.md").exists()
        assert (project_dir / ".github").exists()
        assert not (project_dir / ".gitlab-ci.yml").exists()


def test_generate_gitlab_success():
    runner = CliRunner()
    template_path = str(Path("cookiecutters/consumer").resolve())
    if not os.path.exists(template_path):
        template_path = str(Path("cookiecutters/project").resolve())

    with runner.isolated_filesystem():
        # Provide input manually to select gitlab
        # 1. Name, 2. Slug (Accept Default), 3. Platform (Choose 2 for gitlab), 4-8. Defaults
        inputs = [
            "RegiS GitLab",
            "",  # Accept default slug
            "2",  # Select gitlab
            "",
            "",
            "",
            "",
            "",
        ]
        input_str = "\n".join(inputs) + "\n\n"

        result = runner.invoke(
            main, ["generate", template_path, "test-output"], input=input_str
        )

        if result.exit_code != 0:
            print(f"DEBUG Output:\n{result.output}")

        assert result.exit_code == 0

        # Default slug for "RegiS GitLab" should be "regis-gitlab"
        project_dir = Path("test-output/regis-gitlab")
        assert project_dir.exists()

        if not (project_dir / ".gitlab-ci.yml").exists():
            print(
                f"DEBUG: Files in {project_dir}: {[f.name for f in project_dir.iterdir()]}"
            )

        assert (project_dir / "README.md").exists()
        assert (project_dir / ".gitlab-ci.yml").exists()
        assert not (project_dir / ".github").exists()


def test_generate_invalid_path():
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "nonexistent-template"])
    assert result.exit_code != 0
    assert "does not exist" in result.output.lower()
