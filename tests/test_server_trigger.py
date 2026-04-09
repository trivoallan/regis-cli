"""Tests for regis/server/routes/trigger.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from regis.server.app import create_app


@pytest.fixture()
def assets_dir(tmp_path: Path) -> Path:
    d = tmp_path / "assets"
    d.mkdir()
    (d / "index.html").write_text("<html><body>Dashboard</body></html>")
    return d


@pytest.fixture()
def mock_project() -> MagicMock:
    return MagicMock()


@pytest.fixture()
def client(assets_dir: Path, mock_project: MagicMock):
    with (
        patch("regis.server.routes.trigger._get_project", return_value=mock_project),
        patch("regis.server.routes.gitlab._get_project", return_value=mock_project),
    ):
        app = create_app(
            assets_dir=assets_dir,
            gitlab_url="https://gitlab.com",
            gitlab_token="test-token",
            gitlab_project="123",
        )
        yield TestClient(app), mock_project


class TestTriggerPipeline:
    def test_trigger_success(self, client) -> None:
        test_client, mock_project = client
        mock_pipeline = MagicMock()
        mock_pipeline.attributes = {
            "id": 500,
            "status": "created",
            "web_url": "https://gitlab.com/pipelines/500",
        }
        mock_project.pipelines.create.return_value = mock_pipeline

        resp = test_client.post(
            "/api/gitlab/trigger",
            json={"image_url": "alpine:latest"},
        )

        assert resp.status_code == 200
        data = resp.json()
        assert data["pipeline_id"] == 500
        assert data["status"] == "created"
        assert data["web_url"] == "https://gitlab.com/pipelines/500"

        mock_project.pipelines.create.assert_called_once_with(
            {
                "ref": "main",
                "variables": [
                    {"key": "IMAGE_URL", "value": "alpine:latest"},
                ],
            }
        )

    def test_trigger_custom_ref(self, client) -> None:
        test_client, mock_project = client
        mock_pipeline = MagicMock()
        mock_pipeline.attributes = {
            "id": 501,
            "status": "created",
            "web_url": "https://gitlab.com/pipelines/501",
        }
        mock_project.pipelines.create.return_value = mock_pipeline

        resp = test_client.post(
            "/api/gitlab/trigger",
            json={"image_url": "nginx:latest", "ref": "develop"},
        )

        assert resp.status_code == 200
        mock_project.pipelines.create.assert_called_once_with(
            {
                "ref": "develop",
                "variables": [
                    {"key": "IMAGE_URL", "value": "nginx:latest"},
                ],
            }
        )

    def test_trigger_missing_image_url(self, client) -> None:
        test_client, _ = client
        resp = test_client.post("/api/gitlab/trigger", json={})
        assert resp.status_code == 422  # Validation error

    def test_trigger_not_mounted_without_config(self, assets_dir: Path) -> None:
        app = create_app(assets_dir=assets_dir)
        test_client = TestClient(app)
        resp = test_client.post(
            "/api/gitlab/trigger",
            json={"image_url": "alpine:latest"},
        )
        # No route mounted, SPA fallback returns 405 or index.html
        assert resp.status_code in (200, 405)
