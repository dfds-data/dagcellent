"""Top-level pipeline and airflow config models."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field

from ingestion.models.sql_database import SqlDatabaseSourceConfig

SourceConfig = Annotated[
    SqlDatabaseSourceConfig,
    Field(discriminator="type"),
]


class AirflowSchedules(BaseModel):
    """Per-environment schedule intervals. null = manual trigger only."""

    testing: str | None = None
    staging: str | None = None
    prod: str | None = None


class AirflowConfig(BaseModel):
    """Airflow DAG settings, consumed by the DAG factory."""

    schedules: AirflowSchedules
    start_date: str = "2026-01-01"
    tags: list[str] = Field(default_factory=list)
    owner: str = "compass"
    email: list[str] = Field(default_factory=list)
    dlt_runner_version: str = "latest"


class PipelineConfig(BaseModel):
    """Top-level pipeline configuration, parsed from YAML."""

    name: str
    airflow: AirflowConfig
    source: SourceConfig
