"""Skopeo analyzer — provides raw image metadata using skopeo inspect."""

from __future__ import annotations

import json
import logging
import subprocess
from typing import Any

from regis_cli.analyzers.base import AnalyzerError, BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)


class SkopeoAnalyzer(BaseAnalyzer):
    """Fetch raw metadata for a Docker image using skopeo inspect."""

    name = "skopeo"
    schema_file = "skopeo.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        """Return the raw JSON from skopeo inspect."""
        registry = client.registry
        target = f"docker://{registry}/{repository}:{tag}"

        cmd = [
            "skopeo",
            "inspect",
            "--override-os", "linux",
            "--override-arch", "amd64",
            target,
        ]

        if client.username and client.password:
            cmd.extend(["--creds", f"{client.username}:{client.password}"])

        logger.debug("Running skopeo: %s", " ".join(cmd))

        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            inspect_data = json.loads(res.stdout)
        except subprocess.CalledProcessError as e:
            msg = f"Skopeo inspect failed for {target}: {e.stderr}"
            logger.error(msg)
            raise AnalyzerError(msg) from e
        except FileNotFoundError as e:
            msg = "skopeo not found. Ensure it is installed and in PATH."
            logger.error(msg)
            raise AnalyzerError(msg) from e
        except json.JSONDecodeError as e:
            msg = f"Failed to parse skopeo output for {target}: {res.stdout}"
            logger.error(msg)
            raise AnalyzerError(msg) from e

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "inspect": inspect_data,
        }
