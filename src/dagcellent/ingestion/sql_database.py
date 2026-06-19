"""Pydantic config models for the SQL database source."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from ingestion.base import BaseEntityConfig, BaseSourceConfig


class SqlEntityConfig(BaseEntityConfig):
    """Per-entity ingestion settings for SQL-based sources."""

    included_columns: list[str] | None = None
    row_filter: str | None = None
    chunk_size: int = 50000


class SqlDatabaseSourceConfig(BaseSourceConfig):
    """Source config for SQLAlchemy-compatible databases."""

    type: Literal["sql_database"] = "sql_database"  # type: ignore[assignment]
    database: str
    schema_name: str
    entities: list[SqlEntityConfig] = Field(default_factory=list)
