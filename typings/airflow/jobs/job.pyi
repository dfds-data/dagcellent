"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from functools import cached_property, lru_cache
from typing import TYPE_CHECKING, NoReturn

from airflow.api_internal.internal_api_call import internal_api_call
from airflow.executors.base_executor import BaseExecutor
from airflow.models.base import Base
from airflow.serialization.pydantic.job import JobPydantic
from airflow.traces.tracer import span
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.session import provide_session
from sqlalchemy.orm.session import Session

if TYPE_CHECKING: ...

@lru_cache
def health_check_threshold(job_type: str, heartrate: int) -> int | float: ...

class Job(Base, LoggingMixin):
    """
    The ORM class representing Job stored in the database.

    Jobs are processing items with state and duration that aren't task instances.
    For instance a BackfillJob is a collection of task instance runs,
    but should have its own state, start and end time.
    """

    __tablename__ = ...
    id = ...
    dag_id = ...
    state = ...
    job_type = ...
    start_date = ...
    end_date = ...
    latest_heartbeat = ...
    executor_class = ...
    hostname = ...
    unixname = ...
    __table_args__ = ...
    task_instances_enqueued = ...
    dag_runs = ...
    def __init__(
        self, executor: BaseExecutor | None = ..., heartrate=..., **kwargs
    ) -> None: ...
    @cached_property
    def executor(self):  # -> BaseExecutor:
        ...
    @cached_property
    def executors(self):  # -> list[BaseExecutor]:
        ...
    @cached_property
    def heartrate(self) -> float: ...
    def is_alive(self) -> bool:
        """
        Is this job currently alive.

        We define alive as in a state of RUNNING, and having sent a heartbeat
        within a multiple of the heartrate (default of 2.1)
        """
        ...

    @provide_session
    def kill(self, session: Session = ...) -> NoReturn:
        """Handle on_kill callback and updates state in database."""
        ...

    def on_kill(self):  # -> None:
        """Will be called when an external kill command is received."""
        ...

    @provide_session
    def heartbeat(
        self, heartbeat_callback: Callable[[Session], None], session: Session = ...
    ) -> None:
        """
        Update the job's entry in the database with the latest_heartbeat timestamp.

        This allows for the job to be killed externally and allows the system
        to monitor what is actually active.  For instance, an old heartbeat
        for SchedulerJob would mean something is wrong.  This also allows for
        any job to be killed externally, regardless of who is running it or on
        which machine it is running.

        Note that if your heart rate is set to 60 seconds and you call this
        method after 10 seconds of processing since the last heartbeat, it
        will sleep 50 seconds to complete the 60 seconds and keep a steady
        heart rate. If you go over 60 seconds before calling it, it won't
        sleep at all.

        :param heartbeat_callback: Callback that will be run when the heartbeat is recorded in the Job
        :param session to use for saving the job
        """
        ...

    @provide_session
    def prepare_for_execution(self, session: Session = ...):  # -> None:
        """Prepare the job for execution."""
        ...

    @provide_session
    def complete_execution(self, session: Session = ...):  # -> None:
        ...
    @provide_session
    def most_recent_job(self, session: Session = ...) -> Job | JobPydantic | None:
        """Return the most recent job of this type, if any, based on last heartbeat received."""
        ...

@internal_api_call
@provide_session
def most_recent_job(job_type: str, session: Session = ...) -> Job | JobPydantic | None:
    """
    Return the most recent job of this type, if any, based on last heartbeat received.

    Jobs in "running" state take precedence over others to make sure alive
    job is returned if it is available.

    :param job_type: job type to query for to get the most recent job for
    :param session: Database session
    """
    ...

@provide_session
def run_job(
    job: Job, execute_callable: Callable[[], int | None], session: Session = ...
) -> int | None:
    """
    Run the job.

    The Job is always an ORM object and setting the state is happening within the
    same DB session and the session is kept open throughout the whole execution.

    :meta private:
    """
    ...

def execute_job(job: Job, execute_callable: Callable[[], int | None]) -> int | None:
    """
    Execute the job.

    Job execution requires no session as generally executing session does not require an
    active database connection. The session might be temporary acquired and used if the job
    runs heartbeat during execution, but this connection is only acquired for the time of heartbeat
    and in case of AIP-44 implementation it happens over the Internal API rather than directly via
    the database.

    After the job is completed, state of the Job is updated and it should be updated in the database,
    which happens in the "complete_execution" step (which again can be executed locally in case of
    database operations or over the Internal API call.

    :param job: Job to execute - it can be either DB job or it's Pydantic serialized version. It does
      not really matter, because except of running the heartbeat and state setting,
      the runner should not modify the job state.

    :param execute_callable: callable to execute when running the job.

    :meta private:
    """
    ...

@span
def perform_heartbeat(
    job: Job, heartbeat_callback: Callable[[Session], None], only_if_necessary: bool
) -> None:
    """
    Perform heartbeat for the Job passed to it,optionally checking if it is necessary.

    :param job: job to perform heartbeat for
    :param heartbeat_callback: callback to run by the heartbeat
    :param only_if_necessary: only heartbeat if it is necessary (i.e. if there are things to run for
        triggerer for example)
    """
    ...
