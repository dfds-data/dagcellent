"""Module to help creating Dynamic DAGs in Airflow."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Iterable, List, Optional

import tomli
from pydantic import BaseModel, ConfigDict, ValidationError

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
    schedule: Optional[str] = None
    tags: Optional[List[str]]


class Config(BaseModel):
    """Default config definition.

    Attributes:
        version: (int) version of the parser
        description: (str) short description of the configs (for humans)
    """

    version: int
    description: Optional[str]

    @classmethod
    def from_toml(cls, file: Path) -> Config:
        """
        Function to unpack toml files to Config object.

        Args:
            file (Path): path to toml files.
            test (bool, optional): testing mode. Defaults to False.
        """
        with open(file, "rb") as f:
            k = tomli.load(f)
        return cls(**k)


def parse_config_file(
    resource_paths: Iterable[Path], parser: Callable[..., Config]
) -> List[Config]:
    """
    Open all `TOML` files and returns valid `Config` objects.

    Args:
        resource_paths (Iterable[Path]): file paths
        parser (Callable): parsing logic
    """
    configs: list[Config] = []
    for _path in resource_paths:
        try:
            configs.append(parser(_path))
        except ValidationError as e:
            # we only let the user know about the validation error and continue
            _LOGGER.error("Invalid config file: %s", str(_path), exc_info=e)
            continue
    return configs


if __name__ == "__main__":
    # TODO: turn these into tests

    # test1
    #    _path = (
    #        Path(__file__).parent
    #        / "configs"
    #        / "finance_onprem-to-cloud_findw_full-load.toml"
    #    )
    #    Config.from_toml(_path, True)
    # test2 - should return validation errors and 1 valid dag
    #    _path = (Path(__file__).parent / "configs").glob("**/*.toml")
    #    cfg = parse_config_file(_path, parser=Config.from_toml)
    #    pprint(cfg)
    # test3 - 1 valid dag
    _path = (Path(__file__).parent / "configs").glob("**/*.toml")
    cfg = parse_config_file(_path, parser=Config.from_toml)
