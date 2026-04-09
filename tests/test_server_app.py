"""Tests for regis/server/app.py."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from regis.server.app import create_app


@pytest.fixture()
def assets_dir(tmp_path: Path) -> Path:
    d = tmp_path / "assets"
    d.mkdir()
    (d / "index.html").write_text("<html><body>Dashboard</body></html>")
    return d


class TestHealthEndpoint:
    def test_health(self, assets_dir: Path) -> None:
        app = create_app(assets_dir=assets_dir)
        client = TestClient(app)
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestReportEndpoint:
    def test_report_served_when_provided(
        self, assets_dir: Path, tmp_path: Path
    ) -> None:
        report = tmp_path / "report.json"
        report.write_text(json.dumps({"score": 85}))
        app = create_app(assets_dir=assets_dir, report=report)
        client = TestClient(app)
        resp = client.get("/report.json")
        assert resp.status_code == 200
        assert resp.json() == {"score": 85}

    def test_report_404_when_not_provided(self, assets_dir: Path) -> None:
        app = create_app(assets_dir=assets_dir)
        client = TestClient(app)
        resp = client.get("/report.json")
        assert resp.status_code == 404

    def test_report_404_when_file_missing(
        self, assets_dir: Path, tmp_path: Path
    ) -> None:
        report = tmp_path / "nonexistent.json"
        app = create_app(assets_dir=assets_dir, report=report)
        client = TestClient(app)
        resp = client.get("/report.json")
        assert resp.status_code == 404


class TestArchivesEndpoint:
    def test_archives_served_when_provided(self, assets_dir: Path) -> None:
        archives = [{"name": "Prod", "path": "prod/manifest.json"}]
        app = create_app(assets_dir=assets_dir, archives=archives)
        client = TestClient(app)
        resp = client.get("/archives.json")
        assert resp.status_code == 200
        data = resp.json()
        assert data["archives"] == archives

    def test_archives_404_when_not_provided(self, assets_dir: Path) -> None:
        app = create_app(assets_dir=assets_dir)
        client = TestClient(app)
        resp = client.get("/archives.json")
        assert resp.status_code == 404


class TestSPAFallback:
    def test_index_html_served_at_root(self, assets_dir: Path) -> None:
        app = create_app(assets_dir=assets_dir)
        client = TestClient(app)
        resp = client.get("/")
        assert resp.status_code == 200
        assert "Dashboard" in resp.text

    def test_unknown_path_falls_back_to_index(self, assets_dir: Path) -> None:
        app = create_app(assets_dir=assets_dir)
        client = TestClient(app)
        resp = client.get("/some/nonexistent/route")
        assert resp.status_code == 200
        assert "Dashboard" in resp.text

    def test_static_file_served(self, assets_dir: Path) -> None:
        (assets_dir / "style.css").write_text("body { color: red; }")
        app = create_app(assets_dir=assets_dir)
        client = TestClient(app)
        resp = client.get("/style.css")
        assert resp.status_code == 200
        assert "color: red" in resp.text
