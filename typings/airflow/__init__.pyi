"""
This type stub file was generated by pyright.
"""

import os
import sys
from typing import TYPE_CHECKING

from airflow import settings
from airflow.models.dag import DAG
from airflow.models.dataset import Dataset
from airflow.models.xcom_arg import XComArg

__version__ = ...
if os.environ.get("_AIRFLOW_PATCH_GEVENT"): ...
if sys.platform == "win32": ...
__all__ = ["__version__", "DAG", "Dataset", "XComArg"]
__path__ = ...
if not os.environ.get("_AIRFLOW__AS_LIBRARY", None): ...
__lazy_imports: dict[str, tuple[str, str, bool]] = ...
if TYPE_CHECKING: ...

def __getattr__(name: str):  # -> bool | Any | ModuleType:
    ...

if not settings.LAZY_LOAD_PROVIDERS:
    manager = ...
if not settings.LAZY_LOAD_PLUGINS: ...
