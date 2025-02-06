"""
This type stub file was generated by pyright.
"""

import datetime
from functools import cached_property

from airflow.jobs.base_job_runner import BaseJobRunner
from airflow.utils.pydantic import BaseModel as BaseModelPydantic

def check_runner_initialized(
    job_runner: BaseJobRunner | None, job_type: str
) -> BaseJobRunner: ...

class JobPydantic(BaseModelPydantic):
    """Serializable representation of the Job ORM SqlAlchemyModel used by internal API."""

    id: int | None
    dag_id: str | None
    state: str | None
    job_type: str | None
    start_date: datetime.datetime | None
    end_date: datetime.datetime | None
    latest_heartbeat: datetime.datetime
    executor_class: str | None
    hostname: str | None
    unixname: str | None
    grace_multiplier: float = ...
    model_config = ...
    @cached_property
    def executor(self):  # -> BaseExecutor:
        ...
    @cached_property
    def heartrate(self) -> float: ...
    def is_alive(self) -> bool:
        """Is this job currently alive."""
        ...
