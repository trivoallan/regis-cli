"""HTML report renderer for regis-cli."""

from __future__ import annotations

from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape


def render_html(report: dict[str, Any], theme: str = "default") -> str:
    """Render a full report dict as a standalone HTML page."""
    env = Environment(
        loader=PackageLoader("regis_cli", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Add custom filters
    env.filters["format_number"] = lambda v: f"{v:,}"

    template = env.get_template(f"{theme}/index.html")
    return template.render(report=report, theme=theme)
