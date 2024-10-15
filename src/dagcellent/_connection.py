"""Airflow connection utilities."""
from __future__ import annotations

from enum import Enum


class ConnectionType(str, Enum):
    """Connection type representation.

    Resources:
        [Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#connections)

    """

    MSSQL = "mssql"
    POSTGRES = "postgres"
    REDSHIFT = "redshift"
