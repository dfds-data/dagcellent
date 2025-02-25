"""
This type stub file was generated by pyright.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from airflow.exceptions import RemovedInAirflow3Warning
from airflow.models import TaskInstance
from deprecated import deprecated

"""Task instance APIs."""
if TYPE_CHECKING: ...

@deprecated(
    version="2.2.4",
    reason="Use DagRun.get_task_instance instead",
    category=RemovedInAirflow3Warning,
)
def get_task_instance(
    dag_id: str, task_id: str, execution_date: datetime
) -> TaskInstance:
    """Return the task instance identified by the given dag_id, task_id and execution_date."""
    ...
