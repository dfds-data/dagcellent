"""Tests for pipeline config models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dagcellent.ingestion.pipeline import AirflowConfig, AirflowSchedules, PipelineConfig


class TestAirflowConfig:
    """Test AirflowConfig as part of pipeline."""

    def test_valid_config(self):
        config = AirflowConfig(schedules=AirflowSchedules(prod="0 2 * * *"))
        assert config.start_date == "2026-01-01"
        assert config.owner == "compass"
        assert config.tags == []
        assert config.email == []
        assert config.dlt_runner_version == "latest"

    def test_schedule_defaults_to_manual(self):
        schedules = AirflowSchedules()
        assert schedules.testing is None
        assert schedules.staging is None
        assert schedules.prod is None

    def test_schedules_required(self):
        with pytest.raises(ValidationError):
            AirflowConfig()


class TestPipelineConfig:
    """Test top-level PipelineConfig."""

    def test_valid_pipeline(self):
        """Valid pipeline with airflow and sql source."""
        pipeline = PipelineConfig(
            name="test_ingestion",
            airflow={"schedules": {"prod": "0 2 * * *"}},
            source={
                "type": "sql_database",
                "domain": "test_domain",
                "source_system": "test_source_system",
                "connection_id": "test_conn",
                "database": "test_db",
                "schema_name": "dbo",
            },
        )
        assert pipeline.name == "test_ingestion"
        assert pipeline.airflow.owner == "compass"
        assert pipeline.source.type == "sql_database"

    def test_all_required_fields(self):
        """Missing name, airflow, or source fails."""
        with pytest.raises(ValidationError):
            PipelineConfig(name="test", airflow={"schedules": {}})
