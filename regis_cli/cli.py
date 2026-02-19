"""CLI entry point for regis-cli."""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from importlib import resources
from importlib.metadata import entry_points
from typing import Any

import click
import jsonschema

from regis_cli.analyzers.base import AnalyzerError, BaseAnalyzer
from regis_cli.registry.client import RegistryClient, RegistryError
from regis_cli.registry.parser import parse_image_url
from regis_cli.report.html import render_html

logger = logging.getLogger(__name__)


def _discover_analyzers() -> dict[str, type[BaseAnalyzer]]:
    """Discover all registered analyzers via entry_points."""
    eps = entry_points(group="regis_cli.analyzers")
    discovered: dict[str, type[BaseAnalyzer]] = {}
    for ep in eps:
        try:
            cls = ep.load()
            discovered[ep.name] = cls
        except Exception:
            logger.warning("Failed to load analyzer '%s'", ep.name, exc_info=True)
    return discovered


@click.group()
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose (DEBUG) logging.",
)
def main(verbose: bool) -> None:
    """regis-cli — Docker Registry Analysis CLI."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )


@main.command()
@click.argument("url")
@click.option(
    "-a",
    "--analyzer",
    "analyzer_names",
    multiple=True,
    help="Run only the specified analyzer(s). Can be repeated. Default: all.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    default=None,
    help="Write the JSON report to a file instead of stdout.",
)
@click.option(
    "--pretty/--no-pretty",
    default=True,
    help="Pretty-print the JSON output (default: on).",
)
@click.option(
    "-m",
    "--meta",
    "meta",
    multiple=True,
    help="Arbitrary metadata in key=value format. Can be repeated.",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(["json", "html"], case_sensitive=False),
    default="json",
    help="Output format (default: json).",
)
def analyze(
    url: str,
    analyzer_names: tuple[str, ...],
    output: str | None,
    pretty: bool,
    output_format: str,
    meta: tuple[str, ...],
) -> None:
    """Analyze a Docker image registry.

    URL can be a Docker Hub URL (e.g. https://hub.docker.com/r/library/nginx),
    a bare image reference (nginx:latest), or a private registry URL.
    """
    # Parse the image URL.
    try:
        ref = parse_image_url(url)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(
        f"Analyzing {ref.repository}:{ref.tag} on {ref.registry}",
        err=True,
    )

    # Discover analyzers.
    all_analyzers = _discover_analyzers()
    if not all_analyzers:
        raise click.ClickException(
            "No analyzers found. Is regis-cli installed correctly?"
        )

    # Select which analyzers to run.
    if analyzer_names:
        selected: dict[str, type[BaseAnalyzer]] = {}
        for name in analyzer_names:
            if name not in all_analyzers:
                available = ", ".join(sorted(all_analyzers))
                raise click.ClickException(
                    f"Unknown analyzer '{name}'. Available: {available}"
                )
            selected[name] = all_analyzers[name]
    else:
        selected = all_analyzers

    # Create the registry client.
    client = RegistryClient(
        registry=ref.registry,
        repository=ref.repository,
        username=os.environ.get("REGIS_USERNAME"),
        password=os.environ.get("REGIS_PASSWORD"),
    )

    # Run each analyzer.
    reports: dict[str, Any] = {}
    for name, analyzer_cls in sorted(selected.items()):
        click.echo(f"  Running analyzer: {name}...", err=True)
        analyzer = analyzer_cls()
        try:
            report = analyzer.analyze(client, ref.repository, ref.tag)
            analyzer.validate(report)
            reports[name] = report
        except RegistryError as exc:
            click.echo(f"  ✗ {name}: registry error — {exc}", err=True)
        except AnalyzerError as exc:
            click.echo(f"  ✗ {name}: validation error — {exc}", err=True)

    if not reports:
        raise click.ClickException("All analyzers failed.")

    # Build the final report with request metadata.
    metadata_dict = {}
    for item in meta:
        if "=" in item:
            k, v = item.split("=", 1)
            metadata_dict[k] = v
        else:
            metadata_dict[item] = "true"

    final_report: dict[str, Any] = {
        "request": {
            "url": url,
            "registry": ref.registry,
            "repository": ref.repository,
            "tag": ref.tag,
            "analyzers": sorted(reports.keys()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "results": reports,
    }
    if metadata_dict:
        final_report["metadata"] = metadata_dict

    # Validate final report against its schema.
    schema_text = (
        resources.files("regis_cli.schemas")
        .joinpath("report.schema.json")
        .read_text(encoding="utf-8")
    )
    report_schema = json.loads(schema_text)
    try:
        jsonschema.validate(instance=final_report, schema=report_schema)
    except jsonschema.ValidationError as exc:
        raise click.ClickException(
            f"Report schema validation failed: {exc.message}"
        ) from exc

    # Format output.
    if output_format == "html":
        rendered = render_html(final_report)
    else:
        indent = 2 if pretty else None
        rendered = json.dumps(final_report, indent=indent, ensure_ascii=False)

    if output:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(rendered)
            fh.write("\n")
        click.echo(f"Report written to {output}", err=True)
    else:
        click.echo(rendered)


@main.command(name="list")
def list_analyzers() -> None:
    """List all available analyzers."""
    all_analyzers = _discover_analyzers()
    if not all_analyzers:
        click.echo("No analyzers found.")
        return

    for name, cls in sorted(all_analyzers.items()):
        analyzer = cls()
        click.echo(f"  {name:12s}  {analyzer.__class__.__doc__ or ''}")


@main.command()
@click.argument("url")
@click.option(
    "-s",
    "--scorecard",
    "scorecard_path",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Path to a custom scorecard YAML/JSON file. Default: built-in scorecard.",
)
@click.option(
    "-a",
    "--analyzer",
    "analyzer_names",
    multiple=True,
    help="Run only the specified analyzer(s). Can be repeated. Default: all.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    default=None,
    help="Write the report to a file instead of stdout.",
)
@click.option(
    "-m",
    "--meta",
    "meta",
    multiple=True,
    help="Arbitrary metadata in key=value format. Can be repeated.",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(["json", "html"], case_sensitive=False),
    default="json",
    help="Output format (default: json).",
)
def score(
    url: str,
    scorecard_path: str | None,
    analyzer_names: tuple[str, ...],
    output: str | None,
    output_format: str,
    meta: tuple[str, ...],
) -> None:
    """Evaluate a scorecard against a Docker image.

    Runs all analyzers (or the specified ones), then evaluates a scorecard
    definition against the resulting JSON report.
    Uses JsonLogic rules to determine maturity levels (bronze/silver/gold).

    URL can be a Docker Hub URL, a bare image reference (nginx:latest),
    or a private registry URL.
    """
    from regis_cli.scorecard.engine import evaluate, load_scorecard

    # Parse the image URL.
    try:
        ref = parse_image_url(url)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(
        f"Scoring {ref.repository}:{ref.tag} on {ref.registry}",
        err=True,
    )

    # Discover analyzers.
    all_analyzers = _discover_analyzers()
    if not all_analyzers:
        raise click.ClickException(
            "No analyzers found. Is regis-cli installed correctly?"
        )

    # Select which analyzers to run.
    if analyzer_names:
        selected: dict[str, type[BaseAnalyzer]] = {}
        for name in analyzer_names:
            if name not in all_analyzers:
                available = ", ".join(sorted(all_analyzers))
                raise click.ClickException(
                    f"Unknown analyzer '{name}'. Available: {available}"
                )
            selected[name] = all_analyzers[name]
    else:
        selected = all_analyzers

    # Create the registry client.
    client = RegistryClient(
        registry=ref.registry,
        repository=ref.repository,
        username=os.environ.get("REGIS_USERNAME"),
        password=os.environ.get("REGIS_PASSWORD"),
    )

    # Run each analyzer.
    reports: dict[str, Any] = {}
    for name, analyzer_cls in sorted(selected.items()):
        click.echo(f"  Running analyzer: {name}...", err=True)
        analyzer = analyzer_cls()
        try:
            report = analyzer.analyze(client, ref.repository, ref.tag)
            analyzer.validate(report)
            reports[name] = report
        except RegistryError as exc:
            click.echo(f"  ✗ {name}: registry error — {exc}", err=True)
        except AnalyzerError as exc:
            click.echo(f"  ✗ {name}: validation error — {exc}", err=True)

    if not reports:
        raise click.ClickException("All analyzers failed.")

    # Build the analysis report.
    metadata_dict = {}
    for item in meta:
        if "=" in item:
            k, v = item.split("=", 1)
            metadata_dict[k] = v
        else:
            metadata_dict[item] = "true"

    analysis_report: dict[str, Any] = {
        "request": {
            "url": url,
            "registry": ref.registry,
            "repository": ref.repository,
            "tag": ref.tag,
            "analyzers": sorted(reports.keys()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "results": reports,
    }
    if metadata_dict:
        analysis_report["metadata"] = metadata_dict

    # Load and evaluate scorecard.
    click.echo("  Evaluating scorecard...", err=True)
    sc_def = load_scorecard(scorecard_path)
    sc_result = evaluate(sc_def, analysis_report)

    # Attach scorecard result to the report.
    final_report: dict[str, Any] = {
        **analysis_report,
        "scorecard": sc_result,
    }

    # Render symbols for CLI output.
    level_labels = {
        lv["name"]: lv.get("label", lv["name"]) for lv in sc_def.get("levels", [])
    }
    level_str = level_labels.get(sc_result["level"], sc_result["level"])
    click.echo(
        f"\n  Level: {level_str}  "
        f"({sc_result['passed_rules']}/{sc_result['total_rules']} rules passed, "
        f"{sc_result['score']}%)\n",
        err=True,
    )
    for r in sc_result["rules"]:
        icon = "✅" if r["passed"] else "❌"
        click.echo(f"    {icon} [{r['level']:6s}] {r['title']}", err=True)

    # Format output.
    if output_format == "html":
        rendered = render_html(final_report)
    else:
        rendered = json.dumps(final_report, indent=2, ensure_ascii=False)

    if output:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(rendered)
            fh.write("\n")
        click.echo(f"\nReport written to {output}", err=True)
    else:
        click.echo(rendered)
