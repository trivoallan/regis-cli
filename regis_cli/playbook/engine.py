"""Playbook evaluation engine.

Loads playbook definitions (YAML/JSON) containing scorecards with JsonLogic
conditions and evaluates them against a regis-cli analysis report.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml
from json_logic import jsonLogic

logger = logging.getLogger(__name__)

# Ordered from lowest to highest.
_LEVEL_ORDER = {"bronze": 1, "silver": 2, "gold": 3}


def _flatten(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten a nested dict into dot-separated keys.

    Example::

        {"results": {"tags": {"total_tags": 42}}}
        → {"results.tags.total_tags": 42}
    """
    flat: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(_flatten(value, full_key))
        else:
            flat[full_key] = value
    return flat


def load_playbook(path: str | Path) -> dict[str, Any]:
    """Load a playbook definition from a YAML or JSON file."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    return json.loads(text)


class MissingDataTracker(dict):
    """A dictionary wrapper that tracks which keys were accessed and if they were missing."""

    def __init__(
        self,
        data: dict[str, Any],
        path: str = "",
        root_tracker: MissingDataTracker | None = None,
    ):
        super().__init__(data)
        self.missing_accessed = False
        self.path = path
        # If this is a nested tracker, use the root tracker's accessed_keys set
        if root_tracker:
            self.root = root_tracker
            self.accessed_keys = root_tracker.accessed_keys
        else:
            self.root = self
            self.accessed_keys: set[str] = set()

    def __getitem__(self, key: str) -> Any:
        full_key = f"{self.path}.{key}" if self.path else key
        self.accessed_keys.add(full_key)
        try:
            val = super().__getitem__(key)
        except KeyError:
            self.root.missing_accessed = True
            raise

        if val is None:
            self.root.missing_accessed = True
            return None

        if isinstance(val, dict):
            return MissingDataTracker(val, full_key, self.root)
        return val

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: object) -> bool:
        if isinstance(key, str):
            full_key = f"{self.path}.{key}" if self.path else key
            self.accessed_keys.add(full_key)
        if not super().__contains__(key):
            self.root.missing_accessed = True
            return False
        return True


def _stringify_condition(condition: Any, context: dict[str, Any]) -> str:
    """Turn a JsonLogic condition into a human-readable string with values.

    Example: {">": [{"var": "a"}, 10]} -> "a (42) > 10"
    """
    if not isinstance(condition, dict) or not condition:
        if condition is None:
            return "MISSING"
        return str(condition)

    op = list(condition.keys())[0]
    args = condition[op]

    # Handle var specifically: "key (value)"
    if op == "var":
        val = context.get(args)
        if val is None:
            return f"{args} (MISSING)"
        return f"{args} ({val})"

    if not isinstance(args, list):
        args = [args]

    # Recurse on arguments
    parts = [_stringify_condition(a, context) for a in args]

    # Pretty-print common operators
    if op in (">", ">=", "<", "<=", "==", "!="):
        if len(parts) >= 2:
            return f"{parts[0]} {op} {parts[1]}"
        return f"{op}({', '.join(parts)})"
    if op == "in" and len(parts) == 2:
        return f"{parts[0]} in {parts[1]}"
    if op == "!" and len(parts) == 1:
        return f"!({parts[0]})"
    if op == "and":
        return " and ".join(f"({p})" for p in parts)
    if op == "or":
        return " or ".join(f"({p})" for p in parts)

    return f"{op}({', '.join(parts)})"


def _evaluate_section(
    section: dict[str, Any],
    raw_context: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate a single playbook section against an already-flattened report context.

    Returns a result dict for the section with scorecards, levels_summary, display, etc.
    """
    scorecards_defs = section.get("scorecards", [])

    scorecard_results: list[dict[str, Any]] = []
    for scorecard in scorecards_defs:
        condition = scorecard.get("condition", {})
        tracker = MissingDataTracker(raw_context)
        try:
            result = jsonLogic(condition, tracker)
            passed = bool(result)
            incomplete = tracker.missing_accessed
        except Exception as exc:
            logger.warning(
                "Scorecard '%s' evaluation error: %s",
                scorecard.get("name"),
                exc,
            )
            passed = False
            incomplete = True

        status = "incomplete" if incomplete else ("passed" if passed else "failed")

        involved_analyzers = set()
        for key in tracker.accessed_keys:
            if key.startswith("results."):
                parts = key.split(".")
                if len(parts) > 1:
                    involved_analyzers.add(parts[1])

        scorecard_results.append(
            {
                "name": scorecard.get("name", ""),
                "title": scorecard.get("title", scorecard.get("name", "")),
                "level": scorecard.get("level"),
                "tags": scorecard.get("tags", []),
                "analyzers": sorted(involved_analyzers),
                "passed": passed,
                "status": status,
                "condition": json.dumps(condition),
                "details": _stringify_condition(condition, tracker),
            }
        )

    # Determine summary by level.
    levels_defined = {
        lv["name"]: lv.get("order", _LEVEL_ORDER.get(lv["name"], 0))
        for lv in section.get("levels", [])
    }

    levels_summary = {}
    for level_name in sorted(levels_defined, key=lambda n: levels_defined[n]):
        level_scorecards = [r for r in scorecard_results if r["level"] == level_name]
        if level_scorecards:
            passed_level = sum(1 for r in level_scorecards if r["passed"])
            levels_summary[level_name] = {
                "total": len(level_scorecards),
                "passed": passed_level,
                "percentage": round(passed_level / len(level_scorecards) * 100),
            }

    tags_defined = set()
    for r in scorecard_results:
        for t in r.get("tags", []):
            tags_defined.add(t)

    tags_summary = {}
    for tag_name in sorted(tags_defined):
        tag_scorecards = [r for r in scorecard_results if tag_name in r.get("tags", [])]
        if tag_scorecards:
            passed_tag = sum(1 for r in tag_scorecards if r["passed"])
            tags_summary[tag_name] = {
                "total": len(tag_scorecards),
                "passed": passed_tag,
                "percentage": round(passed_tag / len(tag_scorecards) * 100),
            }

    passed_count = sum(1 for r in scorecard_results if r["passed"])
    total = len(scorecard_results)

    section_result: dict[str, Any] = {
        "name": section.get("name", ""),
        "score": round(passed_count / total * 100) if total else 0,
        "total_scorecards": total,
        "passed_scorecards": passed_count,
        "levels_summary": levels_summary,
        "tags_summary": tags_summary,
        "scorecards": scorecard_results,
    }
    if "hint" in section:
        section_result["hint"] = section["hint"]

    # Resolve display preferences and widget values.
    display = section.get("display")
    if display:
        display_result = dict(display)
        widgets = display_result.get("widgets", [])
        if widgets:
            resolved_widgets = []
            for widget in widgets:
                resolved = dict(widget)
                value_path = widget.get("value")
                if value_path:
                    resolved["resolved_value"] = raw_context.get(value_path)
                resolved_widgets.append(resolved)
            display_result["widgets"] = resolved_widgets
        section_result["display"] = display_result

    # Build render_order from the YAML key order.
    # Python 3.7+ dicts preserve insertion order, so iterating
    # over the section dict reflects the original YAML order.
    render_order: list[str] = []
    for key in section:
        if key == "display":
            display_def = section.get("display", {})
            for display_key in display_def:
                if display_key in ("analyzers", "widgets"):
                    render_order.append(display_key)
        elif key in ("levels", "scorecards"):
            render_order.append(key)

    if tags_summary and "scorecards" in render_order:
        idx = render_order.index("scorecards")
        render_order.insert(idx, "tags")
    elif tags_summary and "tags" not in render_order:
        render_order.append("tags")

    section_result["render_order"] = render_order

    return section_result


def evaluate(
    playbook: dict[str, Any],
    report: dict[str, Any],
    source_name: str | None = None,
) -> dict[str, Any]:
    """Evaluate a playbook against an analysis report.

    Returns a result dict with:
    - ``playbook_name``  — name of the playbook
    - ``sections``       — per-section breakdown (scorecards, levels, display, widgets)
    - ``score``          — overall percentage of scorecards passed (0–100)
    """
    # Build data context.
    raw_context = _flatten(report)
    raw_context.update(report)

    pages_defs = playbook.get("pages")
    sections_defs = playbook.get("sections")

    if not pages_defs and not sections_defs:
        raise ValueError(
            f"Playbook '{playbook.get('name', 'unnamed')}' is missing "
            "both 'pages' and 'sections'. Every playbook must define at least one."
        )

    if not pages_defs:
        # Implicitly wrap root sections in a single defaults page
        pages_defs = [{"name": "Default", "sections": sections_defs}]

    pages_results = []
    total_scorecards_all = 0
    total_passed_all = 0

    for page_def in pages_defs:
        page_sections_defs = page_def.get("sections", [])
        page_sections_results = []
        page_total_scorecards = 0
        page_passed_scorecards = 0

        for section_def in page_sections_defs:
            section_result = _evaluate_section(section_def, raw_context)
            page_sections_results.append(section_result)
            page_total_scorecards += section_result["total_scorecards"]
            page_passed_scorecards += section_result["passed_scorecards"]

        pages_results.append(
            {
                "title": page_def.get("title", "Default"),
                "slug": page_def.get("slug"),
                "score": (
                    round(page_passed_scorecards / page_total_scorecards * 100)
                    if page_total_scorecards
                    else 0
                ),
                "total_scorecards": page_total_scorecards,
                "passed_scorecards": page_passed_scorecards,
                "sections": page_sections_results,
            }
        )
        total_scorecards_all += page_total_scorecards
        total_passed_all += page_passed_scorecards

    # Resolve format strings for any playbook-level links using the report context
    resolved_links = []
    for link_def in playbook.get("links", []):
        if not isinstance(link_def, dict):
            continue

        url_tmpl = link_def.get("url")
        if not isinstance(url_tmpl, str):
            continue

        # Format against original report dictionary
        try:
            url = url_tmpl.format(**report)
            resolved_links.append({"label": link_def.get("label", ""), "url": url})
        except (KeyError, IndexError, ValueError) as e:
            logger.warning(
                "Could not format link '%s': %s",
                link_def.get("label"),
                e,
            )
            # Add as-is if formatting fails, or skip? Let's skip for safety
            # but maybe the user wants it anyway. For now, strictly format it.

    result = {
        "playbook_name": playbook.get("name", "unnamed"),
        "score": (
            round(total_passed_all / total_scorecards_all * 100)
            if total_scorecards_all
            else 0
        ),
        "total_scorecards": total_scorecards_all,
        "passed_scorecards": total_passed_all,
        "pages": pages_results,
        "slug": playbook.get("slug"),
    }

    meta = {}
    if source_name:
        meta["source_name"] = source_name
    if meta:
        result["_meta"] = meta

    if resolved_links:
        result["links"] = resolved_links

    return result
