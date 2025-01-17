"""Mlflow helpers."""

# ruff: noqa: G004
# typing: ignore
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    import mlflow.entities.model_registry


class SlimModelVersion(TypedDict):
    """Slim, JSON serializable type of mlflow.entities.model_registry.ModelVersion."""

    name: str
    version: str
    run_id: str
    tags: dict[str, str]


def serialize_model_version(
    model_version: mlflow.entities.model_registry.ModelVersion,
) -> SlimModelVersion:
    return {
        "name": model_version.name,
        "version": model_version.version,
        "run_id": model_version.run_id,
        "tags": model_version.tags,
    }


class MlflowModelStage(Enum):
    """Allowed Mlflow 'stage' tag values."""

    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"
