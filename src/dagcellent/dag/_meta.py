"""DAG metadata related utilities."""
from __future__ import annotations

import os
from enum import Enum
from pathlib import Path


def get_file_name(path_like: str) -> str:
    """Get current file name.

    Args:
        path_like: use `__file__`

    Returns:
        current file name
    """
    return str(Path(path_like).name).split(".")[0]


def get_parent_name(path_like: str) -> str:
    """Get current file's direct parent.

    Args:
        path_like: use `__file__`

    Returns:
        current file's direct parent
    """
    return str(Path(path_like).parent).split(os.sep)[-1]


def get_dag_id_from_filename(path_like: str) -> str:
    """Get dag name from parent dir and filename.

    Args:
        path_like: use `__file__`

    Returns:
        dag id
    """
    return "_".join([get_parent_name(path_like), get_file_name(path_like)])


class TagBag(str, Enum):
    """Allowed tags.

    For more [see the docs](https://airflow.apache.org/docs/apache-airflow/stable/howto/add-dag-tags.html)

    Attributes:
        cloud: DAG is not running on prem. MutEx with `onprem`.
        onprem: DAG is running on prem. MutEx with `cloud`.
        maintenance: DAG is targeting Airflow maintenance tasks.

    Adding new tags:
        Create a PR to add more tags. Please do not create one-time used tags.
        Tags should be reused for multiple DAGs, so it can be used for
        filtering. The purpose of DAGs should be also understandable, so please
        provide a short description of your tag.
    """

    cloud = "cloud"
    onprem = "onprem"
    maintenance = "maintenance"
