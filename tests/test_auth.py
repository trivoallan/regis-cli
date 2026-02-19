import os
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from regis_cli.cli import main
from regis_cli.registry.client import RegistryClient


class TestRegistryAuth:
    """Test registry authentication logic."""

    def test_client_init_with_credentials(self):
        """Test RegistryClient initialization with credentials."""
        client = RegistryClient(
            "registry.example.com",
            "library/nginx",
            username="user",
            password="password",
        )
        assert client.username == "user"
        assert client.password == "password"

    @patch("regis_cli.registry.client.requests.Session")
    def test_client_authentication_token_request(self, mock_session_cls):
        """Test that credentials are sent during token authentication."""
        mock_session = mock_session_cls.return_value
        
        # Mock 401 response for the initial request
        resp_401 = MagicMock()
        resp_401.status_code = 401
        
        # The WWW-Authenticate header that triggers auth
        resp_401.headers = {
            "WWW-Authenticate": 'Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:library/nginx:pull"'
        }
        
        # Mock 200 response for the token request
        token_resp = MagicMock()
        token_resp.status_code = 200
        token_resp.json.return_value = {"token": "fake-token"}

        # Mock 200 response for the retried request
        resp_200 = MagicMock()
        resp_200.status_code = 200
        resp_200.json.return_value = {}

        # Configure side_effects for session.get
        # 1. Initial request -> 401
        # 2. Token request -> 200
        # 3. Retried request -> 200
        mock_session.get.side_effect = [resp_401, token_resp, resp_200]

        client = RegistryClient(
            "registry.example.com",
            "library/nginx",
            username="myuser",
            password="mypassword",
        )
        
        # Trigger a request that requires auth
        client.list_tags()

        # Verify calls
        assert mock_session.get.call_count == 3
        
        # Check the token request (2nd call)
        token_call = mock_session.get.call_args_list[1]
        args, kwargs = token_call
        
        assert args[0] == "https://auth.docker.io/token"
        assert kwargs["auth"] == ("myuser", "mypassword")

    @patch("regis_cli.cli.jsonschema.validate")
    @patch("regis_cli.cli._discover_analyzers")
    @patch("regis_cli.cli.RegistryClient")
    def test_cli_passes_credentials(self, mock_client_cls, mock_discover, mock_validate):
        """Test that CLI passes credentials from env vars."""
        runner = CliRunner()
        
        # Mock an analyzer setup
        mock_analyzer_cls = MagicMock()
        mock_analyzer_instance = mock_analyzer_cls.return_value
        mock_analyzer_instance.analyze.return_value = {"some": "data"}
        mock_discover.return_value = {"test_analyzer": mock_analyzer_cls}

        env = {
            "REGIS_USERNAME": "env_user",
            "REGIS_PASSWORD": "env_password",
        }
        
        with patch.dict(os.environ, env):
            result = runner.invoke(main, ["analyze", "nginx", "-a", "test_analyzer"])
            
        assert result.exit_code == 0
        
        # Verify RegistryClient was initialized with env credentials
        mock_client_cls.assert_called_once()
        _, kwargs = mock_client_cls.call_args
        
        assert kwargs["username"] == "env_user"
        assert kwargs["password"] == "env_password"

    @patch("regis_cli.cli.jsonschema.validate")
    @patch("regis_cli.scorecard.engine.evaluate")
    @patch("regis_cli.scorecard.engine.load_scorecard")
    @patch("regis_cli.cli._discover_analyzers")
    @patch("regis_cli.cli.RegistryClient")
    def test_score_passes_credentials(self, mock_client_cls, mock_discover, mock_load, mock_eval, mock_validate):
        """Test that score command passes credentials from env vars."""
        runner = CliRunner()
        
        # Mock analyzer
        mock_analyzer_cls = MagicMock()
        mock_analyzer_instance = mock_analyzer_cls.return_value
        mock_analyzer_instance.analyze.return_value = {"some": "data"}
        mock_discover.return_value = {"test_analyzer": mock_analyzer_cls}

        # Mock scorecard
        mock_load.return_value = {"levels": []}
        mock_eval.return_value = {
            "level": "gold",
            "passed_rules": 1,
            "total_rules": 1,
            "score": 100,
            "rules": []
        }

        env = {
            "REGIS_USERNAME": "env_user",
            "REGIS_PASSWORD": "env_password",
        }
        
        with patch.dict(os.environ, env):
            result = runner.invoke(main, ["score", "nginx", "-a", "test_analyzer"])
            
        assert result.exit_code == 0
        
        mock_client_cls.assert_called_once()
        _, kwargs = mock_client_cls.call_args
        
        assert kwargs["username"] == "env_user"
        assert kwargs["password"] == "env_password"
