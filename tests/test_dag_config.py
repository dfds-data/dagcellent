"""Test dynamic DAG configuration."""
from __future__ import annotations

from dagcellent.dynamic_dag import Config

TOML_TEST = """version = 1
description = "test"
"""


def test_config():
    """Test Config."""
    config = Config(version=1, description="test")
    assert config.version == 1
    assert config.description == "test"


def test_extended_config():
    """Test Config."""

    class TestConfig(Config):
        """Test config."""

        test: str

    config = TestConfig(version=1, description="test", test="test")
    assert config.version == 1
    assert config.description == "test"
    assert config.test == "test"
