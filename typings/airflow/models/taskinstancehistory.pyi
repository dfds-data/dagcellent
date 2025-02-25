"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

from airflow.models.base import Base
from airflow.models.taskinstance import TaskInstance
from airflow.serialization.pydantic.taskinstance import TaskInstancePydantic
from airflow.utils.session import NEW_SESSION, provide_session

if TYPE_CHECKING: ...

class TaskInstanceHistory(Base):
    """
    Store old tries of TaskInstances.

    :meta private:
    """

    __tablename__ = ...
    id = ...
    task_id = ...
    dag_id = ...
    run_id = ...
    map_index = ...
    try_number = ...
    start_date = ...
    end_date = ...
    duration = ...
    state = ...
    max_tries = ...
    hostname = ...
    unixname = ...
    job_id = ...
    pool = ...
    pool_slots = ...
    queue = ...
    priority_weight = ...
    operator = ...
    custom_operator_name = ...
    queued_dttm = ...
    queued_by_job_id = ...
    pid = ...
    executor = ...
    executor_config = ...
    updated_at = ...
    rendered_map_index = ...
    external_executor_id = ...
    trigger_id = ...
    trigger_timeout = ...
    next_method = ...
    next_kwargs = ...
    task_display_name = ...
    def __init__(
        self, ti: TaskInstance | TaskInstancePydantic, state: str | None = ...
    ) -> None: ...

    __table_args__ = ...
    @staticmethod
    @provide_session
    def record_ti(ti: TaskInstance, session: NEW_SESSION = ...) -> None:
        """Record a TaskInstance to TaskInstanceHistory."""
        ...
