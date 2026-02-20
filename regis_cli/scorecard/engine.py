"""Scorecard evaluation engine.

Loads scorecard definitions (YAML/JSON) containing rules with JsonLogic
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


def load_scorecard(path: str | Path) -> dict[str, Any]:
    """Load a scorecard definition from a YAML or JSON file."""
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
    """Evaluate a single scorecard section against an already-flattened report context.

    Returns a result dict for the section with rules, levels_summary, display, etc.
    """
    rules_defs = section.get("rules", [])

    rule_results: list[dict[str, Any]] = []
    for rule in rules_defs:
        condition = rule.get("condition", {})
        tracker = MissingDataTracker(raw_context)
        try:
            result = jsonLogic(condition, tracker)
            passed = bool(result)
            incomplete = tracker.missing_accessed
        except Exception as exc:
            logger.warning(
                "Rule '%s' evaluation error: %s",
                rule.get("name"),
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

        rule_results.append(
            {
                "name": rule.get("name", ""),
                "title": rule.get("title", rule.get("name", "")),
                "level": rule.get("level"),
                "tags": rule.get("tags", []),
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
        level_rules = [r for r in rule_results if r["level"] == level_name]
        if level_rules:
            passed_level = sum(1 for r in level_rules if r["passed"])
            levels_summary[level_name] = {
                "total": len(level_rules),
                "passed": passed_level,
                "percentage": round(passed_level / len(level_rules) * 100),
            }

    tags_defined = set()
    for r in rule_results:
        for t in r.get("tags", []):
            tags_defined.add(t)

    tags_summary = {}
    for tag_name in sorted(tags_defined):
        tag_rules = [r for r in rule_results if tag_name in r.get("tags", [])]
        if tag_rules:
            passed_tag = sum(1 for r in tag_rules if r["passed"])
            tags_summary[tag_name] = {
                "total": len(tag_rules),
                "passed": passed_tag,
                "percentage": round(passed_tag / len(tag_rules) * 100),
            }

    passed_count = sum(1 for r in rule_results if r["passed"])
    total = len(rule_results)

    section_result: dict[str, Any] = {
        "name": section.get("name", ""),
        "score": round(passed_count / total * 100) if total else 0,
        "total_rules": total,
        "passed_rules": passed_count,
        "levels_summary": levels_summary,
        "tags_summary": tags_summary,
        "rules": rule_results,
    }

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
        elif key in ("levels", "rules"):
            render_order.append(key)

    if tags_summary and "rules" in render_order:
        idx = render_order.index("rules")
        render_order.insert(idx, "tags")
    elif tags_summary and "tags" not in render_order:
        render_order.append("tags")

    section_result["render_order"] = render_order

    return section_result


def evaluate(
    scorecard: dict[str, Any],
    report: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate a scorecard against an analysis report.

    Returns a result dict with:
    - ``scorecard_name`` — name of the scorecard
    - ``sections``       — per-section breakdown (rules, levels, display, widgets)
    - ``score``          — overall percentage of rules passed (0–100)
    """
    # Build data context.
    raw_context = _flatten(report)
    raw_context.update(report)

    pages_defs = scorecard.get("pages")
    sections_defs = scorecard.get("sections")

    if not pages_defs and not sections_defs:
        raise ValueError(
            f"Scorecard '{scorecard.get('name', 'unnamed')}' is missing "
            "both 'pages' and 'sections'. Every scorecard must define at least one."
        )

    if not pages_defs:
        # Implicitly wrap root sections in a single defaults page
        pages_defs = [{"name": "Default", "sections": sections_defs}]

    pages_results = []
    total_rules_all = 0
    total_passed_all = 0

    for page_def in pages_defs:
        page_sections_defs = page_def.get("sections", [])
        page_sections_results = []
        page_total_rules = 0
        page_passed_rules = 0

        for section_def in page_sections_defs:
            section_result = _evaluate_section(section_def, raw_context)
            page_sections_results.append(section_result)
            page_total_rules += section_result["total_rules"]
            page_passed_rules += section_result["passed_rules"]

        pages_results.append(
            {
                "name": page_def.get("name", "Default"),
                "score": (
                    round(page_passed_rules / page_total_rules * 100)
                    if page_total_rules
                    else 0
                ),
                "total_rules": page_total_rules,
                "passed_rules": page_passed_rules,
                "sections": page_sections_results,
            }
        )
        total_rules_all += page_total_rules
        total_passed_all += page_passed_rules

    # Resolve format strings for any scorecard-level links using the report context
    resolved_links = []
    for link_def in scorecard.get("links", []):
        url_tmpl = link_def.get("url", "")
        # Format against original report dictionary
        try:
            url = url_tmpl.format(**report)
            resolved_links.append({"label": link_def.get("label", ""), "url": url})
        except KeyError as e:
            logger.warning(
                "Could not format link '%s': missing template key %s",
                link_def.get("label"),
                e,
            )
            resolved_links.append(link_def)

    result = {
        "scorecard_name": scorecard.get("name", "unnamed"),
        "score": (
            round(total_passed_all / total_rules_all * 100) if total_rules_all else 0
        ),
        "total_rules": total_rules_all,
        "passed_rules": total_passed_all,
        "pages": pages_results,
    }

    if resolved_links:
        result["links"] = resolved_links

    return result
