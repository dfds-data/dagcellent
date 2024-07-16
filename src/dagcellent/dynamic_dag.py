"""Module to help creating Dynamic DAGs in Airflow."""
from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from pathlib import Path

import tomli
from pydantic import BaseModel, ConfigDict

_LOGGER = logging.getLogger(__name__)


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
    def from_toml(cls, file: Path) -> Config:
        """Load from TOML file to Config object.

        Args:
            file (Path): path to toml files.
            test (bool, optional): testing mode. Defaults to False.
        """
        with open(file, "rb") as f:
            k = tomli.load(f)
        return cls(**k)


def parse_config_file(
    resource_paths: Iterable[Path], parser: Callable[..., Config]
) -> list[Config]:
    """Parse config files.

    Args:
        resource_paths (Iterable[Path]): file paths
        parser (Callable): parsing logic
    """
    configs: list[Config] = []
    for _path in resource_paths:
        configs.append(parser(_path))
    return configs
