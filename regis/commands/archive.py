"""archive command group."""

from __future__ import annotations

import json
from pathlib import Path

import click


def _load_archives_config(path: Path) -> list[dict[str, str]]:
    """Load existing archives.json, returning the archives list."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("archives", [])
    except (json.JSONDecodeError, OSError):
        return []


def _write_archives_config(path: Path, archives: list[dict[str, str]]) -> None:
    """Write archives list to archives.json and validate against schema."""
    import importlib.resources

    import jsonschema

    config = {"archives": archives}

    schema_text = (
        importlib.resources.files("regis") / "schemas" / "archives.schema.json"
    ).read_text(encoding="utf-8")
    schema = json.loads(schema_text)
    jsonschema.validate(config, schema)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


@click.group()
def archive():
    """Manage the report archive."""


@archive.command("add")
@click.argument(
    "report_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option(
    "--archive-dir",
    "-A",
    type=click.Path(file_okay=False, writable=True, path_type=Path),
    required=True,
    help="Archive directory to add the report to.",
)
@click.option(
    "--print-path",
    is_flag=True,
    default=False,
    help="Print only the archived report path to stdout (machine-readable).",
)
def archive_add(report_file: Path, archive_dir: Path, print_path: bool) -> None:
    """Add an existing report JSON file to the archive."""
    from regis.archive.store import add_to_archive

    try:
        report = json.loads(report_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise click.ClickException(f"Could not read {report_file}: {exc}") from exc

    dest = add_to_archive(report, archive_dir)
    if print_path:
        click.echo(dest)
    else:
        click.echo(f"Archived to {dest}", err=True)
        click.echo(f"Manifest updated: {archive_dir / 'manifest.json'}", err=True)


@archive.command("configure")
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default="archives.json",
    show_default=True,
    help="Path to archives.json file.",
)
@click.option(
    "--add",
    "add_entry",
    default=None,
    help='Add an archive non-interactively. Format: "Name:path-or-url".',
)
@click.option(
    "--list",
    "list_archives",
    is_flag=True,
    help="List configured archives and exit.",
)
@click.option(
    "--remove",
    "remove_name",
    default=None,
    help="Remove an archive by name.",
)
def archive_configure(
    output_path: Path,
    add_entry: str | None,
    list_archives: bool,
    remove_name: str | None,
) -> None:
    """Configure multi-archive setup for the dashboard viewer."""
    archives = _load_archives_config(output_path)

    if list_archives:
        if not archives:
            click.echo("No archives configured.", err=True)
        else:
            click.echo(f"Archives in {output_path}:", err=True)
            for a in archives:
                click.echo(f"  {a['name']}: {a['path']}")
        return

    if remove_name:
        before = len(archives)
        archives = [a for a in archives if a["name"] != remove_name]
        if len(archives) == before:
            raise click.ClickException(f"Archive '{remove_name}' not found.")
        _write_archives_config(output_path, archives)
        click.echo(
            f"Removed '{remove_name}'. {len(archives)} archive(s) remaining.", err=True
        )
        return

    if add_entry:
        if ":" not in add_entry:
            raise click.ClickException(
                f'Invalid format: {add_entry!r}. Expected "Name:path-or-url".'
            )
        name, path = add_entry.split(":", 1)
        if not name.strip() or not path.strip():
            raise click.ClickException(
                f"Invalid format: {add_entry!r}. Name and path must not be empty."
            )
        if any(a["name"] == name for a in archives):
            raise click.ClickException(
                f"Archive '{name}' already exists. Remove it first with --remove."
            )
        archives.append({"name": name, "path": path})
        _write_archives_config(output_path, archives)
        click.echo(f"Added '{name}' -> {path}", err=True)
        click.echo(f"Config written to {output_path}", err=True)
        return

    # Interactive mode
    click.echo("Configure archives for the dashboard viewer.\n", err=True)
    if archives:
        click.echo(f"Existing archives in {output_path}:", err=True)
        for a in archives:
            click.echo(f"  {a['name']}: {a['path']}", err=True)
        click.echo("", err=True)

    while True:
        name = click.prompt(
            "Archive name (empty to finish)", default="", show_default=False
        )
        if not name:
            break
        path = click.prompt("  Path or URL")
        if any(a["name"] == name for a in archives):
            click.echo(f"  Archive '{name}' already exists, skipping.", err=True)
            continue
        archives.append({"name": name, "path": path})
        click.echo(f"  Added '{name}' -> {path}", err=True)

    if not archives:
        click.echo("No archives configured. Nothing written.", err=True)
        return

    _write_archives_config(output_path, archives)
    click.echo(
        f"\nConfig written to {output_path} ({len(archives)} archive(s)).", err=True
    )
