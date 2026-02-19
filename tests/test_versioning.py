"""Tests for the versioning analyzer."""

import pytest

from regis_cli.analyzers.versioning import VersioningAnalyzer, _classify_tag


# ---------------------------------------------------------------------------
# Tag classification unit tests
# ---------------------------------------------------------------------------


class TestClassifyTag:
    """Test individual tag classification."""

    @pytest.mark.parametrize("tag,expected", [
        ("1.0.0", "semver"),
        ("v1.0.0", "semver"),
        ("2.4.1", "semver"),
        ("0.1.0", "semver"),
    ])
    def test_semver(self, tag, expected):
        assert _classify_tag(tag) == expected

    @pytest.mark.parametrize("tag,expected", [
        ("1.0.0-alpha", "semver-prerelease"),
        ("v2.0.0-rc.1", "semver-prerelease"),
        ("1.0.0-beta.2", "semver-prerelease"),
    ])
    def test_semver_prerelease(self, tag, expected):
        assert _classify_tag(tag) == expected

    @pytest.mark.parametrize("tag,expected", [
        ("1.88.0-alpine", "semver-variant"),
        ("1.88.0-slim-bookworm", "semver-variant"),
        ("v2.0.0-bullseye", "semver-variant"),
        ("1.91.0-alpine3.21", "semver-variant"),
        ("1.0.0-slim", "semver-variant"),
        ("1.0.0-slim-trixie", "semver-variant"),
    ])
    def test_semver_variant(self, tag, expected):
        assert _classify_tag(tag) == expected

    @pytest.mark.parametrize("tag,expected", [
        ("2024.01", "calver"),
        ("2024.12.25", "calver"),
        ("v2024.06", "calver"),
    ])
    def test_calver(self, tag, expected):
        assert _classify_tag(tag) == expected

    @pytest.mark.parametrize("tag,expected", [
        ("1", "numeric"),
        ("1.2", "numeric"),
        ("v8", "numeric"),
        ("1.27.4.1", "numeric"),
    ])
    def test_numeric(self, tag, expected):
        assert _classify_tag(tag) == expected

    @pytest.mark.parametrize("tag,expected", [
        ("abc1234", "hash"),
        ("deadbeef", "hash"),
        ("a1b2c3d4e5f6", "hash"),
    ])
    def test_hash(self, tag, expected):
        assert _classify_tag(tag) == expected

    @pytest.mark.parametrize("tag,expected", [
        ("latest", "named"),
        ("alpine", "named"),
        ("bookworm-slim", "named"),
        ("1-alpine", "named"),
    ])
    def test_named(self, tag, expected):
        assert _classify_tag(tag) == expected


# ---------------------------------------------------------------------------
# Mock client
# ---------------------------------------------------------------------------


class MockRegistryClient:
    """Minimal mock for RegistryClient."""

    def __init__(self, tags):
        self._tags = tags

    def list_tags(self):
        return sorted(self._tags)


# ---------------------------------------------------------------------------
# Full analyzer tests
# ---------------------------------------------------------------------------


class TestVersioningAnalyzer:
    """Test the versioning analyzer end-to-end."""

    def test_semver_dominant(self):
        tags = ["1.0.0", "1.1.0", "1.2.0", "2.0.0", "2.0.0-rc.1", "latest"]
        client = MockRegistryClient(tags)
        analyzer = VersioningAnalyzer()
        report = analyzer.analyze(client, "library/myapp", "latest")
        analyzer.validate(report)

        assert report["dominant_pattern"] == "semver"
        assert report["total_tags"] == 6
        # 4 semver + 1 prerelease = 5/6 ≈ 83.3%
        assert report["semver_compliant_percentage"] == pytest.approx(83.3, abs=0.1)

    def test_named_dominant(self):
        tags = ["latest", "alpine", "bookworm", "slim"]
        client = MockRegistryClient(tags)
        analyzer = VersioningAnalyzer()
        report = analyzer.analyze(client, "library/python", "latest")
        analyzer.validate(report)

        assert report["dominant_pattern"] == "named"
        assert report["semver_compliant_percentage"] == 0

    def test_mixed_patterns(self):
        tags = ["1.0.0", "1.1.0", "latest", "alpine", "2024.01", "abc1234"]
        client = MockRegistryClient(tags)
        analyzer = VersioningAnalyzer()
        report = analyzer.analyze(client, "test/app", "latest")
        analyzer.validate(report)

        pattern_names = {p["pattern"] for p in report["patterns"]}
        assert "semver" in pattern_names
        assert "named" in pattern_names
        assert "calver" in pattern_names
        assert "hash" in pattern_names

    def test_empty_tags(self):
        client = MockRegistryClient([])
        analyzer = VersioningAnalyzer()
        report = analyzer.analyze(client, "test/empty", "latest")
        analyzer.validate(report)

        assert report["total_tags"] == 0
        assert report["dominant_pattern"] == "unknown"
        assert report["patterns"] == []
