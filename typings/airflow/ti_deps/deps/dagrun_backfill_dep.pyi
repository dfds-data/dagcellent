"""
This type stub file was generated by pyright.
"""

from airflow.ti_deps.deps.base_ti_dep import BaseTIDep

"""This module defines dep for making sure DagRun not a backfill."""

class DagRunNotBackfillDep(BaseTIDep):
    """Dep for valid DagRun run_id to schedule from scheduler."""

    NAME = ...
    IGNORABLE = ...
