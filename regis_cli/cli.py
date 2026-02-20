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


def _format_output_path(template: str, report: dict[str, Any], fmt: str) -> Path:
    """Format an output path template using data from the report."""
    req = report.get("request", {})
    # Provide a 'scorecard' variable if not present directly.
    scorecards = report.get("scorecards", [])
    sc = report.get("scorecard") or (scorecards[0] if scorecards else {})

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
        resolved = template.format(**context)
    except KeyError as exc:
        logger.warning(f"Could not format output path '{template}': missing key {exc}")
        resolved = template

    # Sanitize characters strictly to prevent generating invalid filenames
    sanitized = resolved  # re.sub(r"[^\w\-./\\]+", "_", resolved)

    return Path(sanitized)


def _write_report(
    dir_tmpl: str,
    file_tmpl: str,
    report: dict[str, Any],
    fmt: str,
    rendered: str,
) -> None:
    """Write the rendered report to disk, or fallback if permissions fail."""
    out_dir = _format_output_path(dir_tmpl, report, fmt)
    out_file = _format_output_path(file_tmpl, report, fmt)
    out_path = (out_dir / out_file).resolve()

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        click.echo(f"  Report ({fmt}) written to {out_path}", err=True)
    except PermissionError as exc:
        # If we can't write to the template dir, try current dir as fallback
        fallback_path = Path.cwd() / f"report.{fmt}"
        click.echo(
            f"  Warning: Failed to write to {out_path} ({exc}). Trying fallback to {fallback_path}",
            err=True,
        )
        try:
            fallback_path.write_text(rendered, encoding="utf-8")
            click.echo(f"  Report ({fmt}) written to {fallback_path}", err=True)
        except PermissionError as inner_exc:
            raise click.ClickException(
                f"Failed to write report: Permission denied for both {out_path} and fallback."
            ) from inner_exc


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
    default="reports/{registry}/{repository}/{tag}",
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
    "--theme",
    default="default",
    type=click.Choice(["default"], case_sensitive=False),
    help="Theme to use for HTML report (default: default).",
)
@click.option(
    "--auth",
    "auth",
    multiple=True,
    help="Credentials in registry.domain=user:pass format. Can be repeated.",
)
@click.option(
    "--cache",
    is_flag=True,
    help="Use existing report.json as cache if available.",
)
def analyze(
    url: str,
    analyzer_names: tuple[str, ...],
    scorecard_paths: tuple[str, ...],
    output_template: str | None,
    output_dir_template: str | None,
    pretty: bool,
    output_formats: tuple[str, ...],
    theme: str,
    meta: tuple[str, ...],
    auth: tuple[str, ...],
    cache: bool,
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

    # Select output formats, ensuring 'json' is always generated.
    formats_set = {f.lower() for f in output_formats} if output_formats else set()
    formats_set.add("json")
    # Put json first, then others
    formats = ["json"] + sorted(list(formats_set - {"json"}))

    # 1. Check for cache if requested.
    final_report = None
    if cache:
        # Construct the expected path for a JSON report to see if it exists.
        # We use a dummy report to get the path.
        dummy_report = {
            "request": {
                "registry": ref.registry,
                "repository": ref.repository,
                "tag": ref.tag,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        }
        dir_tmpl = output_dir_template or "reports/{registry}/{repository}/{tag}"
        file_tmpl = output_template or "report.{format}"

        try:
            cache_dir = _format_output_path(dir_tmpl, dummy_report, "json")
            cache_file = _format_output_path(file_tmpl, dummy_report, "json")
            cache_path = cache_dir / cache_file

            if cache_path.exists():
                click.echo(f"  Using cached report from {cache_path}", err=True)
                final_report = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.debug("Cache lookup failed: %s", exc)

    if final_report:
        # If we have a cached report, we skip analysis and scorecard evaluation.
        # We might want to re-run scorecards eventually, but for now we follow the "cache report" intent.
        pass
    else:
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

        from regis_cli.registry.auth import resolve_credentials

        # Create the registry client.
        username, password = resolve_credentials(
            ref.registry, list(auth) if auth else None
        )
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
                sc_result = evaluate(
                    sc_def, analysis_report, source_name=Path(sc_path).stem
                )
                scorecard_results.append(sc_result)

                # Print summary for EACH scorecard if in CLI mode
                if "html" not in formats or len(formats) > 1:
                    summary_parts = []
                    for section in sc_result.get("sections", []):
                        for lv_name, stats in section.get("levels_summary", {}).items():
                            summary_parts.append(
                                f"{lv_name}: {stats['passed']}/{stats['total']}"
                            )

                    summary_str = " · ".join(summary_parts)
                    click.echo(
                        f"    {summary_str}  "
                        f"({sc_result['passed_rules']}/{sc_result['total_rules']} rules passed, "
                        f"{sc_result['score']}%)\n",
                        err=True,
                    )

        # Build the final report.
        final_report = {
            **analysis_report,
        }
        if scorecard_results:
            final_report["scorecards"] = scorecard_results
            # For backward compatibility (or simplicity), keep 'scorecard' pointing to the first result.
            final_report["scorecard"] = scorecard_results[0]

        # Extract evaluated links from scorecards
        all_links = []
        for sc_res in scorecard_results:
            for link_def in sc_res.get("links", []):
                if link_def not in all_links:
                    all_links.append(link_def)

        if all_links:
            final_report["links"] = all_links

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
            # For HTML, generate one file per scorecard if scorecards exist.
            # If no scorecards, generate a single report using fallback logic.
            if scorecard_results:
                for sc in scorecard_results:
                    # Render HTML focusing on this single scorecard.
                    # We pass the full report, but we might want to tell the template which SC to focus on,
                    # or temporarily set 'scorecards' to just this one for rendering.
                    single_sc_report = {
                        **final_report,
                        "scorecards": [sc],
                        "scorecard": sc,
                    }
                    rendered = render_html(single_sc_report, theme=theme)

                    # Determine filename for this scorecard
                    file_tmpl = output_template
                    if not file_tmpl:
                        if sc.get("slug"):
                            file_tmpl = f"{sc['slug']}.{fmt}"
                        elif "_meta" in sc and sc["_meta"].get("source_name"):
                            file_tmpl = f"{sc['_meta']['source_name']}.{fmt}"
                        else:
                            file_tmpl = (
                                f"report_{sc.get('scorecard_name', 'unnamed')}.{fmt}"
                            )

                    _write_report(
                        dir_tmpl=output_dir_template or ".",
                        file_tmpl=file_tmpl,
                        report=single_sc_report,
                        fmt=fmt,
                        rendered=rendered,
                    )
            else:
                # No scorecards, just render the base report
                rendered = render_html(final_report, theme=theme)
                file_tmpl = output_template or f"report.{fmt}"
                _write_report(
                    dir_tmpl=output_dir_template or ".",
                    file_tmpl=file_tmpl,
                    report=final_report,
                    fmt=fmt,
                    rendered=rendered,
                )
        else:
            # JSON (and other formats): Single unified report file
            indent = 2 if pretty else None
            rendered = json.dumps(final_report, indent=indent, ensure_ascii=False)
            file_tmpl = output_template or f"report.{fmt}"
            _write_report(
                dir_tmpl=output_dir_template or ".",
                file_tmpl=file_tmpl,
                report=final_report,
                fmt=fmt,
                rendered=rendered,
            )


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
