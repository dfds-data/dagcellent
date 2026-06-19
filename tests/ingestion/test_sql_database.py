"""Tests for SQL database ingestion config models.

Covers: SqlDatabaseSourceConfig, SqlEntityConfig.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dagcellent.ingestion.sql_database import SqlDatabaseSourceConfig, SqlEntityConfig

@pytest.fixture
def source_config():
    return SqlDatabaseSourceConfig(
        domain="test_domain",
        source_system="test_system",
        connection_id="test_conn",
        database="test_db",
        schema_name="test_schema",
    )


@pytest.fixture
def entity_config():
    return SqlEntityConfig(name="test_entity", write_disposition="append")


class TestSqlDatabaseSourceConfig:
    def test_valid_config(self):
        assert source_config.type == "sql_database"
        assert source_config.database == "test_db"
        assert source_config.schema_name == "test_schema"
        assert source_config.entities == []

    def test_type_is_fixed(self, source_config):
        assert source_config.type == "sql_database"

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError) as exc:
            SqlDatabaseSourceConfig(
                source_system="test_system", connection_id="test_conn", database="test_db"
            )
        assert "domain" in str(exc.value)
    def test_validate_raw_source_config() -> None:
        raw = {
            "type": "sql_database",
            "domain": "test_domain",
            "source_system": "test_system",
            "connection_id": "test_conn",
            "database": "test_db",
            "schema_name": "test_schema",
        }
        config = SqlDatabaseSourceConfig.model_validate(raw)
        assert isinstance(config, SqlDatabaseSourceConfig)

class TestSqlEntityConfig:
    def test_defaults(self, entity_config):
        assert entity_config.partition_column is None
        assert entity_config.incremental_column is None
        assert entity_config.included_columns is None
        assert entity_config.row_filter is None
        assert entity_config.chunk_size == 50000

    def test_schema_contract_default(self):
        assert entity_config.schema_contract == {"data_type": "evolve", "columns": "evolve"}

    def test_schema_contract_override(self):
        entity = SqlEntityConfig(
            name="test_entity",
            write_disposition="append",
            schema_contract={"data_type": "freeze", "columns": "freeze"},
        )
        assert entity.schema_contract == {"data_type": "freeze", "columns": "freeze"}

    def test_invalid_write_disposition(self):
        with pytest.raises(ValidationError):
            SqlEntityConfig(name="test_entity", write_disposition="invalid")

    def test_valid_write_dispositions(self):
        for disposition in ("append", "replace"):
            entity = SqlEntityConfig(name="test_entity", write_disposition=disposition)
            assert entity.write_disposition == disposition


def test_valid_entity_config(entity_config: SqlEntityConfig) -> None:
    assert entity_config.name == "test_entity"
    assert entity_config.write_disposition == "append"
    assert entity_config.chunk_size == 50000
    assert entity_config.included_columns is None
    assert entity_config.row_filter is None


def test_validate_raw_entity_config_missing_required_field() -> None:
    with pytest.raises(ValidationError):
        SqlEntityConfig.model_validate({"name": "test_entity"})

