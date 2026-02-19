"""Tests for the scorecard evaluation engine."""

from __future__ import annotations

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

    def test_load_default(self):
        sc = load_scorecard()
        assert sc["name"] == "Image Health"
        assert len(sc["rules"]) == 9
        assert len(sc["levels"]) == 3

    def test_load_from_file(self, tmp_path):
        custom = {
            "name": "Custom",
            "levels": [
                {"name": "bronze", "order": 1},
            ],
            "rules": [
                {
                    "name": "test-rule",
                    "title": "A test rule",
                    "level": "bronze",
                    "condition": {"==": [1, 1]},
                },
            ],
        }
        p = tmp_path / "custom.yaml"
        p.write_text(yaml.dump(custom))
        loaded = load_scorecard(p)
        assert loaded["name"] == "Custom"
        assert len(loaded["rules"]) == 1

    def test_load_json(self, tmp_path):
        import json
        custom = {
            "name": "JSON Card",
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
        p = tmp_path / "custom.json"
        p.write_text(json.dumps(custom))
        loaded = load_scorecard(p)
        assert loaded["name"] == "JSON Card"


class TestEvaluate:
    """Test scorecard evaluation."""

    SCORECARD = {
        "name": "Test Scorecard",
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
                "condition": {"==": [{"var": "results.provenance.has_provenance"}, True]},
            },
            {
                "name": "good-score",
                "title": "Good scorecard",
                "level": "gold",
                "condition": {">=": [{"var": "results.scorecarddev.score"}, 7]},
            },
        ],
    }

    def test_all_pass_gold(self):
        report = {
            "results": {
                "tags": {"total_tags": 100},
                "provenance": {"has_provenance": True},
                "scorecarddev": {"score": 8},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["level"] == "gold"
        assert result["score"] == 100
        assert result["passed_rules"] == 3
        assert all(r["passed"] for r in result["rules"])

    def test_bronze_only(self):
        report = {
            "results": {
                "tags": {"total_tags": 50},
                "provenance": {"has_provenance": False},
                "scorecarddev": {"score": 2},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["level"] == "bronze"
        assert result["passed_rules"] == 1

    def test_silver_level(self):
        report = {
            "results": {
                "tags": {"total_tags": 50},
                "provenance": {"has_provenance": True},
                "scorecarddev": {"score": 3},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["level"] == "silver"
        assert result["passed_rules"] == 2

    def test_none_level(self):
        report = {
            "results": {
                "tags": {"total_tags": 0},
                "provenance": {"has_provenance": False},
                "scorecarddev": {"score": 0},
                "trivy": {"vulnerability_count": 100},
            },
        }
        result = evaluate(self.SCORECARD, report)
        assert result["level"] == "none"
        assert result["passed_rules"] == 0

    def test_empty_rules(self):
        result = evaluate({"name": "empty", "rules": []}, {})
        assert result["level"] == "none"
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
        assert result["level"] == "none"
        # Some rules might pass if var returns None and comparison works
        # but the important thing is no exception is raised.
        assert isinstance(result["score"], int)
