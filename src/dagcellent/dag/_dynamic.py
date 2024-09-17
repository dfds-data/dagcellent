"""Module to help creating Dynamic DAGs in Airflow."""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import TypeVar

import tomli
from pydantic import BaseModel, ConfigDict

T = TypeVar("T", bound="Config")


class DagArguments(BaseModel):
    """Airflow DAG args, kwargs.

    Attributes:
        dag_id: (str) DAG id
        description: (str)
        schedule: (str) dag run schedule
        tags: dag tags
        default_args: airflow.Task default arguments read the list of
          arguments [here](https://airflow.apache.org/docs/apache-airflow/2.9.1/_api/airflow/models/baseoperator/index.html).

    """

    model_config = ConfigDict(extra="allow")

    dag_id: str
    description: str
    schedule: str | None = None
    tags: list[str] | None


class Config(BaseModel):
    """Default config definition.

    Attributes:
        version: (int) version of the parser
        description: (str) short description of the configs (for humans)
    """

    version: int
    description: str | None

    @classmethod
    def from_toml(cls: type[T], file: Path) -> T:
        """Load from TOML file to Config object.

        Args:
            file (Path): path to toml files.
        """
        with open(file, "rb") as f:
            k = tomli.load(f)
        return cls(**k)

    @classmethod
    def from_json(cls: type[T], file: Path) -> T:
        """Load from JSON file to Config object.

        Args:
            file (Path): path to toml files.
        """
        with open(file) as f:
            k = json.load(f)
        return cls(**k)


def parse_config_file(
    resource_paths: Iterable[Path], parser: Callable[..., T]
) -> list[T]:
    """Parse config files.

    Args:
        resource_paths (Iterable[Path]): file paths
        parser (Callable): parsing logic
    """
    configs: list[T] = []
    for _path in resource_paths:
        configs.append(parser(_path))
    return configs
