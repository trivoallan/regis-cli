"""Tests for the scorecard evaluation engine."""

from __future__ import annotations

import pytest
import yaml

from regis_cli.scorecard.engine import _flatten, evaluate, load_scorecard


class TestFlatten:
    """Test the ``_flatten`` helper."""

    def test_simple(self):
        data = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
        flat = _flatten(data)
        assert flat == {"a": 1, "b.c": 2, "b.d.e": 3}

    def test_empty(self):
        assert _flatten({}) == {}


class TestLoadScorecard:
    """Test scorecard loading."""

    def test_load_from_file(self, tmp_path):
        custom = {
            "name": "Custom",
            "sections": [
                {
                    "name": "Main",
                    "levels": [{"name": "bronze", "order": 1}],
                    "rules": [
                        {
                            "name": "test-rule",
                            "title": "A test rule",
                            "level": "bronze",
                            "condition": {"==": [1, 1]},
                        },
                    ],
                }
            ],
        }
        p = tmp_path / "custom.yaml"
        p.write_text(yaml.dump(custom))
        loaded = load_scorecard(p)
        assert loaded["name"] == "Custom"
        assert len(loaded["sections"][0]["rules"]) == 1

    def test_load_json(self, tmp_path):
        import json

        custom = {
            "name": "JSON Card",
            "sections": [
                {
                    "name": "Main",
                    "levels": [{"name": "bronze", "order": 1}],
                    "rules": [
                        {
                            "name": "always-pass",
                            "title": "Always passes",
                            "level": "bronze",
                            "condition": {"==": [1, 1]},
                        },
                    ],
                }
            ],
        }
        p = tmp_path / "custom.json"
        p.write_text(json.dumps(custom))
        loaded = load_scorecard(p)
        assert loaded["name"] == "JSON Card"


class TestEvaluate:
    """Test scorecard evaluation."""

    SCORECARD = {
        "name": "Test Scorecard",
        "sections": [
            {
                "name": "Test",
                "levels": [
                    {"name": "bronze", "order": 1},
                    {"name": "silver", "order": 2},
                    {"name": "gold", "order": 3},
                ],
                "rules": [
                    {
                        "name": "has-tags",
                        "title": "Has tags",
                        "level": "bronze",
                        "condition": {">": [{"var": "results.tags.total_tags"}, 0]},
                    },
                    {
                        "name": "has-provenance",
                        "title": "Has provenance",
                        "level": "silver",
                        "condition": {
                            "==": [{"var": "results.provenance.has_provenance"}, True]
                        },
                    },
                    {
                        "name": "good-score",
                        "title": "Good scorecard",
                        "level": "gold",
                        "condition": {">=": [{"var": "results.scorecarddev.score"}, 7]},
                    },
                ],
            }
        ],
    }

    def test_all_pass(self):
        report = {
            "results": {
                "tags": {"total_tags": 100},
                "provenance": {"has_provenance": True},
                "scorecarddev": {"score": 8},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["score"] == 100
        assert result["passed_rules"] == 3
        section = result["pages"][0]["sections"][0]
        assert all(r["passed"] for r in section["rules"])

    def test_partial_pass(self):
        report = {
            "results": {
                "tags": {"total_tags": 50},
                "provenance": {"has_provenance": False},
                "scorecarddev": {"score": 2},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["passed_rules"] == 1

    def test_two_pass(self):
        report = {
            "results": {
                "tags": {"total_tags": 50},
                "provenance": {"has_provenance": True},
                "scorecarddev": {"score": 3},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["passed_rules"] == 2

    def test_tags_propagation(self):
        """Test that tags are correctly copied from rule defs to results."""
        scorecard = {
            "name": "Tags Test",
            "sections": [
                {
                    "name": "Main",
                    "rules": [
                        {
                            "name": "rule-with-tags",
                            "tags": ["tag1", "tag2"],
                            "condition": {"==": [1, 1]},
                        },
                        {
                            "name": "rule-without-tags",
                            "condition": {"==": [1, 1]},
                        },
                    ],
                }
            ],
        }
        result = evaluate(scorecard, {})
        rules = result["pages"][0]["sections"][0]["rules"]
        assert rules[0]["tags"] == ["tag1", "tag2"]
        assert rules[1]["tags"] == []

    def test_incomplete_status(self):
        """Test that missing data results in an 'incomplete' status."""
        scorecard = {
            "name": "Missing Data Test",
            "sections": [
                {
                    "name": "Main",
                    "rules": [
                        {
                            "name": "missing-var",
                            "condition": {">": [{"var": "non_existent"}, 0]},
                        }
                    ],
                }
            ],
        }
        result = evaluate(scorecard, {"some_other_data": 42})
        rules = result["pages"][0]["sections"][0]["rules"]
        assert rules[0]["status"] == "incomplete"
        assert "MISSING" in rules[0]["details"]

    def test_no_pass(self):
        report = {
            "results": {
                "tags": {"total_tags": 0},
                "provenance": {"has_provenance": False},
                "scorecarddev": {"score": 0},
                "trivy": {"vulnerability_count": 100},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["passed_rules"] == 0

    def test_empty_rules(self):
        result = evaluate(
            {"name": "empty", "sections": [{"name": "Main", "rules": []}]}, {}
        )
        assert result["score"] == 0

    def test_score_percentage(self):
        report = {
            "results": {
                "tags": {"total_tags": 10},
                "provenance": {"has_provenance": True},
                "scorecarddev": {"score": 3},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["score"] == 67  # 2/3 = 66.67 → rounds to 67

    def test_missing_data_fails_gracefully(self):
        """Rules referencing missing data should fail, not crash."""
        report = {"results": {}}
        result = evaluate(self.SCORECARD, report)
        assert isinstance(result["score"], int)

    def test_missing_sections_raises(self):
        """Scorecards without sections must raise ValueError."""
        scorecard = {
            "name": "Legacy",
            "rules": [{"name": "r", "condition": {"==": [1, 1]}}],
        }
        with pytest.raises(ValueError, match="missing both 'pages' and 'sections'"):
            evaluate(scorecard, {})

    def test_multi_section(self):
        """Multiple sections aggregate correctly."""
        scorecard = {
            "name": "Multi",
            "sections": [
                {
                    "name": "A",
                    "rules": [
                        {"name": "a1", "title": "A1", "condition": {"==": [1, 1]}},
                    ],
                },
                {
                    "name": "B",
                    "rules": [
                        {"name": "b1", "title": "B1", "condition": {"==": [1, 0]}},
                    ],
                },
            ],
        }
        result = evaluate(scorecard, {})
        assert result["total_rules"] == 2
        assert result["passed_rules"] == 1
        assert result["score"] == 50
        assert len(result["pages"][0]["sections"]) == 2

    def test_render_order(self):
        """render_order reflects the YAML key definition order."""
        scorecard = {
            "name": "Order Test",
            "sections": [
                {
                    "name": "Rules First",
                    "rules": [
                        {"name": "r1", "title": "R1", "condition": {"==": [1, 1]}},
                    ],
                    "display": {
                        "widgets": [{"label": "W", "value": "x"}],
                        "analyzers": ["trivy"],
                    },
                    "levels": [{"name": "bronze", "order": 1}],
                },
            ],
        }
        result = evaluate(scorecard, {})
        order = result["pages"][0]["sections"][0]["render_order"]
        assert order == ["rules", "widgets", "analyzers", "levels"]
