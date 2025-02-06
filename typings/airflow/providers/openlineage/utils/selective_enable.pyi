"""
This type stub file was generated by pyright.
"""

from typing import TypeVar

from airflow.models import DAG, Operator

ENABLE_OL_PARAM_NAME = ...
ENABLE_OL_PARAM = ...
DISABLE_OL_PARAM = ...
T = TypeVar("T", bound="DAG | Operator")
log = ...

def enable_lineage(obj: T) -> T:
    """
    Set selective enable OpenLineage parameter to True.

    The method also propagates param to tasks if the object is DAG.
    """
    ...

def disable_lineage(obj: T) -> T:
    """
    Set selective enable OpenLineage parameter to False.

    The method also propagates param to tasks if the object is DAG.
    """
    ...

def is_task_lineage_enabled(task: Operator) -> bool:
    """Check if selective enable OpenLineage parameter is set to True on task level."""
    ...

def is_dag_lineage_enabled(dag: DAG) -> bool:
    """
    Check if DAG is selectively enabled to emit OpenLineage events.

    The method also checks if selective enable parameter is set to True
    or if any of the tasks in DAG is selectively enabled.
    """
    ...
