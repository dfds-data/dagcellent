"""
This type stub file was generated by pyright.
"""

from collections.abc import Collection, Iterable
from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple

from airflow.models.dag import DAG
from airflow.models.dagrun import DagRun
from airflow.models.operator import Operator
from airflow.models.taskinstance import TaskInstance
from airflow.utils.session import provide_session
from airflow.utils.state import DagRunState, TaskInstanceState
from sqlalchemy.orm import Session as SASession

"""Marks tasks APIs."""
if TYPE_CHECKING: ...

class _DagRunInfo(NamedTuple):
    logical_date: datetime
    data_interval: tuple[datetime, datetime]
    ...

@provide_session
def set_state(
    *,
    tasks: Collection[Operator | tuple[Operator, int]],
    run_id: str | None = ...,
    execution_date: datetime | None = ...,
    upstream: bool = ...,
    downstream: bool = ...,
    future: bool = ...,
    past: bool = ...,
    state: TaskInstanceState = ...,
    commit: bool = ...,
    session: SASession = ...,
) -> list[TaskInstance]:
    """
    Set the state of a task instance and if needed its relatives.

    Can set state for future tasks (calculated from run_id) and retroactively
    for past tasks. Will verify integrity of past dag runs in order to create
    tasks that did not exist. It will not create dag runs that are missing
    on the schedule (but it will, as for subdag, dag runs if needed).

    :param tasks: the iterable of tasks or (task, map_index) tuples from which to work.
        ``task.dag`` needs to be set
    :param run_id: the run_id of the dagrun to start looking from
    :param execution_date: the execution date from which to start looking (deprecated)
    :param upstream: Mark all parents (upstream tasks)
    :param downstream: Mark all siblings (downstream tasks) of task_id, including SubDags
    :param future: Mark all future tasks on the interval of the dag up until
        last execution date.
    :param past: Retroactively mark all tasks starting from start_date of the DAG
    :param state: State to which the tasks need to be set
    :param commit: Commit tasks to be altered to the database
    :param session: database session
    :return: list of tasks that have been created and updated
    """
    ...

def all_subdag_tasks_query(
    sub_dag_run_ids: list[str],
    session: SASession,
    state: TaskInstanceState,
    confirmed_dates: Iterable[datetime],
):
    """Get *all* tasks of the sub dags."""
    ...

def get_all_dag_task_query(
    dag: DAG,
    session: SASession,
    state: TaskInstanceState,
    task_ids: list[str | tuple[str, int]],
    run_ids: Iterable[str],
):
    """Get all tasks of the main dag that will be affected by a state change."""
    ...

def verify_dagruns(
    dag_runs: Iterable[DagRun],
    commit: bool,
    state: DagRunState,
    session: SASession,
    current_task: Operator,
):  # -> None:
    """
    Verify integrity of dag_runs.

    :param dag_runs: dag runs to verify
    :param commit: whether dag runs state should be updated
    :param state: state of the dag_run to set if commit is True
    :param session: session to use
    :param current_task: current task
    """
    ...

def find_task_relatives(
    tasks, downstream, upstream
):  # -> Generator[tuple[Any, Any] | Any, Any, None]:
    """Yield task ids and optionally ancestor and descendant ids."""
    ...

@provide_session
def get_execution_dates(
    dag: DAG,
    execution_date: datetime,
    future: bool,
    past: bool,
    *,
    session: SASession = ...,
) -> list[datetime]:
    """Return DAG execution dates."""
    ...

@provide_session
def get_run_ids(
    dag: DAG, run_id: str, future: bool, past: bool, session: SASession = ...
):  # -> list[Any] | list[str] | list[Any | str | None]:
    """Return DAG executions' run_ids."""
    ...

@provide_session
def set_dag_run_state_to_success(
    *,
    dag: DAG,
    execution_date: datetime | None = ...,
    run_id: str | None = ...,
    commit: bool = ...,
    session: SASession = ...,
) -> list[TaskInstance]:
    """
    Set the dag run's state to success.

    Set for a specific execution date and its task instances to success.

    :param dag: the DAG of which to alter state
    :param execution_date: the execution date from which to start looking(deprecated)
    :param run_id: the run_id to start looking from
    :param commit: commit DAG and tasks to be altered to the database
    :param session: database session
    :return: If commit is true, list of tasks that have been updated,
             otherwise list of tasks that will be updated
    :raises: ValueError if dag or execution_date is invalid
    """
    ...

@provide_session
def set_dag_run_state_to_failed(
    *,
    dag: DAG,
    execution_date: datetime | None = ...,
    run_id: str | None = ...,
    commit: bool = ...,
    session: SASession = ...,
) -> list[TaskInstance]:
    """
    Set the dag run's state to failed.

    Set for a specific execution date and its task instances to failed.

    :param dag: the DAG of which to alter state
    :param execution_date: the execution date from which to start looking(deprecated)
    :param run_id: the DAG run_id to start looking from
    :param commit: commit DAG and tasks to be altered to the database
    :param session: database session
    :return: If commit is true, list of tasks that have been updated,
             otherwise list of tasks that will be updated
    :raises: AssertionError if dag or execution_date is invalid
    """
    ...

@provide_session
def set_dag_run_state_to_running(
    *,
    dag: DAG,
    execution_date: datetime | None = ...,
    run_id: str | None = ...,
    commit: bool = ...,
    session: SASession = ...,
) -> list[TaskInstance]:
    """
    Set the dag run's state to running.

    Set for a specific execution date and its task instances to running.
    """
    ...

@provide_session
def set_dag_run_state_to_queued(
    *,
    dag: DAG,
    execution_date: datetime | None = ...,
    run_id: str | None = ...,
    commit: bool = ...,
    session: SASession = ...,
) -> list[TaskInstance]:
    """
    Set the dag run's state to queued.

    Set for a specific execution date and its task instances to queued.
    """
    ...
