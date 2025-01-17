"""Test dynamic DAG configuration."""

from __future__ import annotations

import pathlib

import pytest
from pydantic import ValidationError

from dagcellent.dag import Config, parse_config_file


def test_config():
    """Test Config."""
    config = Config(version=1, description="test")
    assert config.version == 1
    assert config.description == "test"


def test_extended_config():
    """Test sub-classing."""

    class TestConfig(Config):
        """Test config."""

        test: str

    config = TestConfig(version=1, description="test", test="test")
    assert config.version == 1
    assert config.description == "test"
    assert config.test == "test"


def test_config_from_toml(toml_file: pathlib.Path):
    """Test Config.load."""
    config = Config.from_toml(toml_file)
    assert config.version == 1
    assert config.description == "test"


def test_parse_config_file(toml_file: pathlib.Path):
    """Test the end API."""
    # only one file passed
    with pytest.raises(TypeError):
        assert parse_config_file(pathlib.Path(), Config.from_toml)  # type: ignore[arg-type]

    with pytest.raises(FileNotFoundError):
        assert parse_config_file([pathlib.Path("dummy.toml")], Config.from_toml)

    class MyConfig(Config):
        """My config."""

        test: str

    with pytest.raises(ValidationError):
        assert parse_config_file([toml_file], MyConfig.from_toml)

    config = parse_config_file([toml_file], Config.from_toml)
    assert config[0].version == 1
    assert config[0].description == "test"


def test_parse_json_config_file(json_file: pathlib.Path):
    """Test the end API."""
    # only one file passed
    with pytest.raises(TypeError):
        assert parse_config_file(pathlib.Path(), Config.from_json)  # type: ignore[arg-type]

    with pytest.raises(FileNotFoundError):
        assert parse_config_file([pathlib.Path("dummy.toml")], Config.from_json)

    class MyConfig(Config):
        """My config."""

        test: str

    with pytest.raises(ValidationError):
        assert parse_config_file([json_file], MyConfig.from_json)

    config = parse_config_file([json_file], Config.from_json)
    assert config[0].version == 1
    assert config[0].description == "test"
