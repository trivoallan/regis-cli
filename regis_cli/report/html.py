"""HTML report renderer for regis-cli."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

logger = logging.getLogger(__name__)


def render_html(report: dict[str, Any], theme: str = "default") -> str:
    """Render a full report dict as a standalone HTML page."""
    env = Environment(
        loader=PackageLoader("regis_cli", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Add custom filters
    env.filters["format_number"] = lambda v: f"{v:,}"

    def _format_date(v: str) -> str:
        try:
            return datetime.fromisoformat(v).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return v

    def _format_datetime(v: str) -> str:
        try:
            return datetime.fromisoformat(v).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return v

    def _format_time(v: str) -> str:
        try:
            return datetime.fromisoformat(v).strftime("%H:%M:%S")
        except (ValueError, TypeError):
            return v

    env.filters["format_date"] = _format_date
    env.filters["format_datetime"] = _format_datetime
    env.filters["format_time"] = _format_time

    template = env.get_template(f"{theme}/index.html")
    return template.render(report=report, theme=theme)
