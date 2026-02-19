"""CLI entry point for regis-cli."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from importlib import resources
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any

import click
import jsonschema

from regis_cli.analyzers.base import AnalyzerError, BaseAnalyzer
from regis_cli.registry.client import RegistryClient, RegistryError
from regis_cli.registry.parser import parse_image_url

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


def _format_output_path(template: str, data: dict[str, Any], fmt: str) -> Path:
    """Format an output path template using report data."""
    req = data.get("request", {})
    # Use first scorecard for placeholders if multiple exist
    scorecards = data.get("scorecards", [])
    sc = scorecards[0] if scorecards else data.get("scorecard", {})

    # Sanitize repository name for filesystem
    repo = req.get("repository", "unknown").replace("/", "-").replace(":", "-")

    # Format timestamp for filesystem
    ts_str = req.get("timestamp", "")
    try:
        ts = datetime.fromisoformat(ts_str)
        timestamp = ts.strftime("%Y%m%d-%H%M%S")
    except (ValueError, TypeError):
        timestamp = ts_str.replace(":", "-")

    context = {
        "repository": repo,
        "tag": req.get("tag", "latest"),
        "registry": req.get("registry", "unknown"),
        "timestamp": timestamp,
        "format": fmt,
        "level": sc.get("level", "none"),
        "score": sc.get("score", 0),
    }

    try:
        path_str = template.format(**context)
    except KeyError as exc:
        raise click.ClickException(
            f"Invalid placeholder in output template: {exc}"
        ) from exc

    return Path(path_str)


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
    "-s",
    "--scorecard",
    "scorecard_paths",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to custom scorecard YAML/JSON file(s). Can be repeated. Default: built-in scorecard.",
)
@click.option(
    "-o",
    "--output",
    "output_template",
    help="Output filename template (e.g. 'report.{format}'). If not provided and one format requested, outputs to stdout.",
)
@click.option(
    "-D",
    "--output-dir",
    "output_dir_template",
    help="Base directory template for output files (e.g. 'reports/{repository}').",
    default="reports/{repository}/{tag}",
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
    "output_formats",
    multiple=True,
    type=click.Choice(["json", "html"], case_sensitive=False),
    help="Output format (can be repeated, default: json).",
)
@click.option(
    "--auth",
    "auth",
    multiple=True,
    help="Credentials in registry.domain=user:pass format. Can be repeated.",
)
def analyze(
    url: str,
    analyzer_names: tuple[str, ...],
    scorecard_paths: tuple[str, ...],
    output_template: str | None,
    output_dir_template: str | None,
    pretty: bool,
    output_formats: tuple[str, ...],
    meta: tuple[str, ...],
    auth: tuple[str, ...],
) -> None:
    """Analyze a Docker image and evaluate scorecards.

    URL can be a Docker Hub URL (e.g. https://hub.docker.com/r/library/nginx),
    a bare image reference (nginx:latest), or a private registry URL.

    Runs analyzers and evaluates one or more scorecards against the results.
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

    # Select output formats.
    formats = [f.lower() for f in output_formats] if output_formats else ["json"]

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

    from regis_cli.registry.auth import resolve_credentials

    # Create the registry client.
    username, password = resolve_credentials(ref.registry, list(auth) if auth else None)
    client = RegistryClient(
        registry=ref.registry,
        repository=ref.repository,
        username=username,
        password=password,
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
            reports[name] = {
                "analyzer": name,
                "error": {"type": "registry", "message": str(exc)},
            }
        except AnalyzerError as exc:
            click.echo(f"  ✗ {name}: validation error — {exc}", err=True)
            reports[name] = {
                "analyzer": name,
                "error": {"type": "validation", "message": str(exc)},
            }
        except Exception as exc:
            click.echo(f"  ✗ {name}: unexpected error — {exc}", err=True)
            reports[name] = {
                "analyzer": name,
                "error": {"type": "unexpected", "message": str(exc)},
            }

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

    # Load and evaluate scorecards.
    from regis_cli.scorecard.engine import evaluate, load_scorecard

    scorecard_results = []
    if scorecard_paths:
        for sc_path in scorecard_paths:
            click.echo(f"  Evaluating scorecard: {sc_path}...", err=True)
            sc_def = load_scorecard(sc_path)
            sc_result = evaluate(sc_def, analysis_report)
            scorecard_results.append(sc_result)

            # Print summary for EACH scorecard if in CLI mode
            if "html" not in formats or len(formats) > 1:
                level_labels = {
                    lv["name"]: lv.get("label", lv["name"])
                    for lv in sc_def.get("levels", [])
                }
                summary_parts = []
                for lv_name, stats in sc_result["levels_summary"].items():
                    label = level_labels.get(lv_name, lv_name)
                    summary_parts.append(f"{label}: {stats['passed']}/{stats['total']}")

                summary_str = " · ".join(summary_parts)
                click.echo(
                    f"    {summary_str}  "
                    f"({sc_result['passed_rules']}/{sc_result['total_rules']} rules passed, "
                    f"{sc_result['score']}%)\n",
                    err=True,
                )

    # Build the final report.
    final_report: dict[str, Any] = {
        **analysis_report,
    }
    if scorecard_results:
        final_report["scorecards"] = scorecard_results
        # For backward compatibility (or simplicity), keep 'scorecard' pointing to the first result.
        final_report["scorecard"] = scorecard_results[0]

    # Validate final report against its schema.
    from jsonschema.validators import validator_for
    from referencing import Registry, Resource

    schemas_dir = resources.files("regis_cli.schemas")
    registry = Registry()
    report_schema = None
    base_uri = "https://regis-cli/schemas/"

    for schema_file in schemas_dir.iterdir():
        if not schema_file.name.endswith(".json"):
            continue
        schema_data = json.loads(schema_file.read_text(encoding="utf-8"))
        resource = Resource.from_contents(schema_data)

        # Register both by filename (relative) and by $id if available.
        registry = registry.with_resource(uri=schema_file.name, resource=resource)
        registry = registry.with_resource(
            uri=base_uri + schema_file.name, resource=resource
        )
        if "$id" in schema_data:
            registry = registry.with_resource(uri=schema_data["$id"], resource=resource)

        if schema_file.name == "report.schema.json":
            report_schema = schema_data

    if report_schema:
        try:
            validator_cls = validator_for(report_schema)
            validator = validator_cls(report_schema, registry=registry)
            validator.validate(instance=final_report)
        except jsonschema.ValidationError as exc:
            raise click.ClickException(
                f"Report schema validation failed: {exc.message}"
            ) from exc

    # Format and write outputs.
    from regis_cli.report.html import render_html

    for fmt in formats:
        if fmt == "html":
            rendered = render_html(final_report)
        else:
            indent = 2 if pretty else None
            rendered = json.dumps(final_report, indent=indent, ensure_ascii=False)

        # Determine if we should write to file or stdout
        if output_template or output_dir_template or len(formats) > 1:
            # Use templates or defaults
            dir_tmpl = output_dir_template or "."
            file_tmpl = output_template or "report.{format}"

            out_dir = _format_output_path(dir_tmpl, final_report, fmt)
            out_file = _format_output_path(file_tmpl, final_report, fmt)
            out_path = out_dir / out_file

            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(rendered, encoding="utf-8")
            click.echo(f"Report ({fmt}) written to {out_path}", err=True)
        else:
            # Single format, no template/dir -> stdout
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
