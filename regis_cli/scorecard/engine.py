"""Scorecard evaluation engine.

Loads scorecard definitions (YAML/JSON) containing rules with JsonLogic
conditions and evaluates them against a regis-cli analysis report.
"""

from __future__ import annotations

import json
import logging
from collections import UserDict
from importlib import resources
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


def load_scorecard(path: str | Path | None = None) -> dict[str, Any]:
    """Load a scorecard definition from a YAML or JSON file.

    If *path* is ``None`` the built-in default scorecard is loaded.
    """
    if path is None:
        default = (
            resources.files("regis_cli.scorecard")
            .joinpath("default.yaml")
            .read_text(encoding="utf-8")
        )
        return yaml.safe_load(default)

    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    return json.loads(text)


from collections import UserDict


class MissingDataTracker(UserDict):
    """A dictionary wrapper that tracks if None values were accessed."""

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.missing_accessed = False

    def __getitem__(self, key: str) -> Any:
        try:
            val = self.data[key]
            if val is None:
                self.missing_accessed = True
            return val
        except KeyError:
            self.missing_accessed = True
            return None

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except (KeyError, IndexError):
            return default


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
        val = context.get(args, "None")
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


def evaluate(
    scorecard: dict[str, Any],
    report: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate a scorecard against an analysis report.

    Returns a result dict with:
    - ``scorecard_name`` — name of the scorecard
    - ``level``          — highest achieved level (or ``"none"``)
    - ``score``          — percentage of rules passed (0–100)
    - ``rules``          — per-rule breakdown
    """
    rules_defs = scorecard.get("rules", [])
    if not rules_defs:
        return {
            "scorecard_name": scorecard.get("name", "unnamed"),
            "level": "none",
            "score": 0,
            "total_rules": 0,
            "passed_rules": 0,
            "rules": [],
        }

    # Build data context — both the nested original *and* a flat version
    # so that JsonLogic ``var`` can use dot paths like
    # ``results.tags.total_tags``.
    raw_context = _flatten(report)
    # Also keep the nested structure for advanced rules.
    raw_context.update(report)

    rule_results: list[dict[str, Any]] = []
    for rule in rules_defs:
        condition = rule.get("condition", {})
        # Use a tracker to detect if None values are accessed during evaluation
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

        rule_results.append(
            {
                "name": rule.get("name", ""),
                "title": rule.get("title", rule.get("name", "")),
                "level": rule.get("level", "bronze"),
                "tags": rule.get("tags", []),
                "passed": passed,
                "status": status,
                "condition": json.dumps(condition),
                "details": _stringify_condition(condition, tracker),
            }
        )

    # Determine achieved level: a level is achieved when ALL rules at
    # that level *and all lower levels* pass.
    levels_defined = {
        lv["name"]: lv.get("order", _LEVEL_ORDER.get(lv["name"], 0))
        for lv in scorecard.get("levels", [])
    }
    if not levels_defined:
        levels_defined = dict(_LEVEL_ORDER)

    achieved = "none"
    for level_name in sorted(levels_defined, key=lambda n: levels_defined[n]):
        # All rules at this level or below must pass.
        threshold = levels_defined[level_name]
        relevant = [
            r for r in rule_results if levels_defined.get(r["level"], 0) <= threshold
        ]
        if relevant and all(r["passed"] for r in relevant):
            achieved = level_name

    passed_count = sum(1 for r in rule_results if r["passed"])
    total = len(rule_results)

    return {
        "scorecard_name": scorecard.get("name", "unnamed"),
        "level": achieved,
        "score": round(passed_count / total * 100) if total else 0,
        "total_rules": total,
        "passed_rules": passed_count,
        "rules": rule_results,
    }
