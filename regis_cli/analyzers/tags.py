"""Tags analyzer — lists available tags for a repository."""

from __future__ import annotations

from typing import Any

from regis_cli.analyzers.base import BaseAnalyzer
from regis_cli.registry.client import RegistryClient


class TagsAnalyzer(BaseAnalyzer):
    """List all tags available for a Docker image repository."""

    name = "tags"
    schema_file = "tags.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        """Return a report with all available tags.

        The *tag* argument is ignored — this analyzer lists every tag
        in the repository.
        """
        tags = client.list_tags()
        return {
            "analyzer": self.name,
            "repository": repository,
            "tags": tags,
            "count": len(tags),
        }
