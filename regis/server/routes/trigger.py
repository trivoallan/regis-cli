"""Pipeline trigger route for the regis dashboard server."""

from __future__ import annotations

import logging

import gitlab
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from regis.server.routes.gitlab import GitLabConfig, _get_project

logger = logging.getLogger(__name__)


class TriggerRequest(BaseModel):
    """Request body for triggering a pipeline analysis."""

    image_url: str = Field(
        ..., description="Container image to analyze (e.g. alpine:latest)"
    )
    ref: str = Field(default="main", description="Branch to run the pipeline on")


class TriggerResponse(BaseModel):
    """Response after triggering a pipeline."""

    pipeline_id: int
    status: str
    web_url: str


def create_trigger_router(config: GitLabConfig) -> APIRouter:
    """Create a FastAPI router for pipeline trigger endpoints.

    Args:
        config: GitLab connection configuration.
    """
    router = APIRouter(prefix="/api/gitlab", tags=["gitlab"])

    @router.post("/trigger", response_model=TriggerResponse)
    async def trigger_pipeline(body: TriggerRequest) -> TriggerResponse:
        """Trigger a GitLab pipeline with IMAGE_URL variable."""
        project = _get_project(config)
        try:
            pipeline = project.pipelines.create(
                {
                    "ref": body.ref,
                    "variables": [
                        {"key": "IMAGE_URL", "value": body.image_url},
                    ],
                }
            )
        except gitlab.GitlabCreateError as exc:
            raise HTTPException(
                status_code=502, detail=f"Failed to trigger pipeline: {exc}"
            ) from exc

        attrs = pipeline.attributes if hasattr(pipeline, "attributes") else pipeline
        return TriggerResponse(
            pipeline_id=attrs["id"],
            status=attrs["status"],
            web_url=attrs["web_url"],
        )

    return router
