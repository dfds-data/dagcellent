"""
This type stub file was generated by pyright.
"""

import contextlib
from collections.abc import Callable, Collection, Generator, Iterable
from datetime import datetime
from enum import Enum
from pathlib import PurePath
from types import TracebackType
from typing import TYPE_CHECKING, Any

import jinja2
import pendulum
from airflow.api_internal.internal_api_call import internal_api_call
from airflow.exceptions import RemovedInAirflow3Warning, TaskDeferred
from airflow.models.base import Base, TaskInstanceDependencies
from airflow.models.baseoperator import BaseOperator
from airflow.models.dag import DAG, DagModel
from airflow.models.dagrun import DagRun
from airflow.models.operator import Operator
from airflow.models.taskinstancekey import TaskInstanceKey
from airflow.models.taskreschedule import TaskReschedule
from airflow.serialization.pydantic.taskinstance import TaskInstancePydantic
from airflow.ti_deps.dep_context import DepContext
from airflow.typing_compat import Literal
from airflow.utils.context import Context
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.session import provide_session
from airflow.utils.state import DagRunState, TaskInstanceState
from deprecated import deprecated
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import reconstructor
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.expression import ColumnOperators

TR = TaskReschedule
_CURRENT_CONTEXT: list[Context] = ...
log = ...
if TYPE_CHECKING: ...
PAST_DEPENDS_MET = ...

class TaskReturnCode(Enum):
    """
    Enum to signal manner of exit for task run command.

    :meta private:
    """

    DEFERRED = ...

@contextlib.contextmanager
def set_current_context(context: Context) -> Generator[Context, None, None]:
    """
    Set the current execution context to the provided context object.

    This method should be called once per Task execution, before calling operator.execute.
    """
    ...

def clear_task_instances(
    tis: list[TaskInstance],
    session: Session,
    activate_dag_runs: None = ...,
    dag: DAG | None = ...,
    dag_run_state: DagRunState | Literal[False] = ...,
) -> None:
    """
    Clear a set of task instances, but make sure the running ones get killed.

    Also sets Dagrun's `state` to QUEUED and `start_date` to the time of execution.
    But only for finished DRs (SUCCESS and FAILED).
    Doesn't clear DR's `state` and `start_date`for running
    DRs (QUEUED and RUNNING) because clearing the state for already
    running DR is redundant and clearing `start_date` affects DR's duration.

    :param tis: a list of task instances
    :param session: current session
    :param dag_run_state: state to set finished DagRuns to.
        If set to False, DagRuns state will not be changed.
    :param dag: DAG object
    :param activate_dag_runs: Deprecated parameter, do not pass
    """
    ...

class TaskInstance(Base, LoggingMixin):
    """
    Task instances store the state of a task instance.

    This table is the authority and single source of truth around what tasks
    have run and the state they are in.

    The SqlAlchemy model doesn't have a SqlAlchemy foreign key to the task or
    dag model deliberately to have more control over transactions.

    Database transactions on this table should insure double triggers and
    any confusion around what task instances are or aren't ready to run
    even while multiple schedulers may be firing task instances.

    A value of -1 in map_index represents any of: a TI without mapped tasks;
    a TI with mapped tasks that has yet to be expanded (state=pending);
    a TI with mapped tasks that expanded to an empty list (state=skipped).
    """

    __tablename__ = ...
    task_id = ...
    dag_id = ...
    run_id = ...
    map_index = ...
    start_date = ...
    end_date = ...
    duration = ...
    state = ...
    try_number = ...
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
    _task_display_property_value = ...
    __table_args__ = ...
    dag_model: DagModel = ...
    trigger = ...
    triggerer_job = ...
    dag_run = ...
    rendered_task_instance_fields = ...
    execution_date = ...
    task_instance_note = ...
    note = ...
    task: Operator | None = ...
    test_mode: bool = ...
    is_trigger_log_context: bool = ...
    run_as_user: str | None = ...
    raw: bool | None = ...
    _logger_name = ...
    def __init__(
        self,
        task: Operator,
        execution_date: datetime | None = ...,
        run_id: str | None = ...,
        state: str | None = ...,
        map_index: int = ...,
    ) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def stats_tags(self) -> dict[str, str]:
        """Returns task instance tags."""
        ...

    @staticmethod
    def insert_mapping(run_id: str, task: Operator, map_index: int) -> dict[str, Any]:
        """
        Insert mapping.

        :meta private:
        """
        ...

    @reconstructor
    def init_on_load(self) -> None:
        """Initialize the attributes that aren't stored in the DB."""
        ...

    @property
    @deprecated(
        reason="Use try_number instead.",
        version="2.10.0",
        category=RemovedInAirflow3Warning,
    )
    def prev_attempted_tries(self) -> int:
        """
        Calculate the total number of attempted tries, defaulting to 0.

        This used to be necessary because try_number did not always tell the truth.

        :meta private:
        """
        ...

    @property
    def next_try_number(self) -> int: ...
    @property
    def operator_name(self) -> str | None:
        """@property: use a more friendly display name for the operator, if set."""
        ...

    @hybrid_property
    def task_display_name(self) -> str: ...
    def command_as_list(
        self,
        mark_success: bool = ...,
        ignore_all_deps: bool = ...,
        ignore_task_deps: bool = ...,
        ignore_depends_on_past: bool = ...,
        wait_for_past_depends_before_skipping: bool = ...,
        ignore_ti_state: bool = ...,
        local: bool = ...,
        pickle_id: int | None = ...,
        raw: bool = ...,
        job_id: str | None = ...,
        pool: str | None = ...,
        cfg_path: str | None = ...,
    ) -> list[str]:
        """
        Return a command that can be executed anywhere where airflow is installed.

        This command is part of the message sent to executors by the orchestrator.
        """
        ...

    @staticmethod
    def generate_command(
        dag_id: str,
        task_id: str,
        run_id: str,
        mark_success: bool = ...,
        ignore_all_deps: bool = ...,
        ignore_depends_on_past: bool = ...,
        wait_for_past_depends_before_skipping: bool = ...,
        ignore_task_deps: bool = ...,
        ignore_ti_state: bool = ...,
        local: bool = ...,
        pickle_id: int | None = ...,
        file_path: PurePath | str | None = ...,
        raw: bool = ...,
        job_id: str | None = ...,
        pool: str | None = ...,
        cfg_path: str | None = ...,
        map_index: int = ...,
    ) -> list[str]:
        """
        Generate the shell command required to execute this task instance.

        :param dag_id: DAG ID
        :param task_id: Task ID
        :param run_id: The run_id of this task's DagRun
        :param mark_success: Whether to mark the task as successful
        :param ignore_all_deps: Ignore all ignorable dependencies.
            Overrides the other ignore_* parameters.
        :param ignore_depends_on_past: Ignore depends_on_past parameter of DAGs
            (e.g. for Backfills)
        :param wait_for_past_depends_before_skipping: Wait for past depends before marking the ti as skipped
        :param ignore_task_deps: Ignore task-specific dependencies such as depends_on_past
            and trigger rule
        :param ignore_ti_state: Ignore the task instance's previous failure/success
        :param local: Whether to run the task locally
        :param pickle_id: If the DAG was serialized to the DB, the ID
            associated with the pickled DAG
        :param file_path: path to the file containing the DAG definition
        :param raw: raw mode (needs more details)
        :param job_id: job ID (needs more details)
        :param pool: the Airflow pool that the task should run in
        :param cfg_path: the Path to the configuration file
        :return: shell command that can be used to run the task instance
        """
        ...

    @property
    def log_url(self) -> str:
        """Log URL for TaskInstance."""
        ...

    @property
    def mark_success_url(self) -> str:
        """URL to mark TI success."""
        ...

    @provide_session
    def current_state(self, session: Session = ...) -> str:
        """
        Get the very latest state from the database.

        If a session is passed, we use and looking up the state becomes part of the session,
        otherwise a new session is used.

        sqlalchemy.inspect is used here to get the primary keys ensuring that if they change
        it will not regress

        :param session: SQLAlchemy ORM Session
        """
        ...

    @provide_session
    def error(self, session: Session = ...) -> None:
        """
        Force the task instance's state to FAILED in the database.

        :param session: SQLAlchemy ORM Session
        """
        ...

    @classmethod
    @internal_api_call
    @provide_session
    def get_task_instance(
        cls,
        dag_id: str,
        run_id: str,
        task_id: str,
        map_index: int,
        lock_for_update: bool = ...,
        session: Session = ...,
    ) -> TaskInstance | TaskInstancePydantic | None: ...
    @provide_session
    def refresh_from_db(
        self, session: Session = ..., lock_for_update: bool = ...
    ) -> None:
        """
        Refresh the task instance from the database based on the primary key.

        :param session: SQLAlchemy ORM Session
        :param lock_for_update: if True, indicates that the database should
            lock the TaskInstance (issuing a FOR UPDATE clause) until the
            session is committed.
        """
        ...

    def refresh_from_task(
        self, task: Operator, pool_override: str | None = ...
    ) -> None:
        """
        Copy common attributes from the given task.

        :param task: The task object to copy from
        :param pool_override: Use the pool_override instead of task's pool
        """
        ...

    @provide_session
    def clear_xcom_data(self, session: Session = ...):  # -> None:
        ...
    @property
    def key(self) -> TaskInstanceKey:
        """Returns a tuple that identifies the task instance uniquely."""
        ...

    @provide_session
    def set_state(self, state: str | None, session: Session = ...) -> bool:
        """
        Set TaskInstance state.

        :param state: State to set for the TI
        :param session: SQLAlchemy ORM Session
        :return: Was the state changed
        """
        ...

    @property
    def is_premature(self) -> bool:
        """Returns whether a task is in UP_FOR_RETRY state and its retry interval has elapsed."""
        ...

    @provide_session
    def are_dependents_done(self, session: Session = ...) -> bool:
        """
        Check whether the immediate dependents of this task instance have succeeded or have been skipped.

        This is meant to be used by wait_for_downstream.

        This is useful when you do not want to start processing the next
        schedule of a task until the dependents are done. For instance,
        if the task DROPs and recreates a table.

        :param session: SQLAlchemy ORM Session
        """
        ...

    @provide_session
    def get_previous_dagrun(
        self, state: DagRunState | None = ..., session: Session | None = ...
    ) -> DagRun | None:
        """
        Return the DagRun that ran before this task instance's DagRun.

        :param state: If passed, it only take into account instances of a specific state.
        :param session: SQLAlchemy ORM Session.
        """
        ...

    @provide_session
    def get_previous_ti(
        self, state: DagRunState | None = ..., session: Session = ...
    ) -> TaskInstance | TaskInstancePydantic | None:
        """
        Return the task instance for the task that ran before this task instance.

        :param session: SQLAlchemy ORM Session
        :param state: If passed, it only take into account instances of a specific state.
        """
        ...

    @property
    def previous_ti(self) -> TaskInstance | TaskInstancePydantic | None:
        """
        This attribute is deprecated.

        Please use :class:`airflow.models.taskinstance.TaskInstance.get_previous_ti`.
        """
        ...

    @property
    def previous_ti_success(self) -> TaskInstance | TaskInstancePydantic | None:
        """
        This attribute is deprecated.

        Please use :class:`airflow.models.taskinstance.TaskInstance.get_previous_ti`.
        """
        ...

    @provide_session
    def get_previous_execution_date(
        self, state: DagRunState | None = ..., session: Session = ...
    ) -> pendulum.DateTime | None:
        """
        Return the execution date from property previous_ti_success.

        :param state: If passed, it only take into account instances of a specific state.
        :param session: SQLAlchemy ORM Session
        """
        ...

    @provide_session
    def get_previous_start_date(
        self, state: DagRunState | None = ..., session: Session = ...
    ) -> pendulum.DateTime | None:
        """
        Return the start date from property previous_ti_success.

        :param state: If passed, it only take into account instances of a specific state.
        :param session: SQLAlchemy ORM Session
        """
        ...

    @property
    def previous_start_date_success(self) -> pendulum.DateTime | None:
        """
        This attribute is deprecated.

        Please use :class:`airflow.models.taskinstance.TaskInstance.get_previous_start_date`.
        """
        ...

    @provide_session
    def are_dependencies_met(
        self,
        dep_context: DepContext | None = ...,
        session: Session = ...,
        verbose: bool = ...,
    ) -> bool:
        """
        Are all conditions met for this task instance to be run given the context for the dependencies.

        (e.g. a task instance being force run from the UI will ignore some dependencies).

        :param dep_context: The execution context that determines the dependencies that should be evaluated.
        :param session: database session
        :param verbose: whether log details on failed dependencies on info or debug log level
        """
        ...

    @provide_session
    def get_failed_dep_statuses(
        self, dep_context: DepContext | None = ..., session: Session = ...
    ):  # -> Generator[TIDepStatus | Any, Any, None]:
        """Get failed Dependencies."""
        ...

    def __repr__(self) -> str: ...
    def next_retry_datetime(self):
        """
        Get datetime of the next retry if the task instance fails.

        For exponential backoff, retry_delay is used as base and will be converted to seconds.
        """
        ...

    def ready_for_retry(self) -> bool:
        """Check on whether the task instance is in the right state and timeframe to be retried."""
        ...

    @provide_session
    def get_dagrun(self, session: Session = ...) -> DagRun:
        """
        Return the DagRun for this TaskInstance.

        :param session: SQLAlchemy ORM Session
        :return: DagRun
        """
        ...

    @classmethod
    @provide_session
    def ensure_dag(
        cls, task_instance: TaskInstance | TaskInstancePydantic, session: Session = ...
    ) -> DAG:
        """Ensure that task has a dag object associated, might have been removed by serialization."""
        ...

    @provide_session
    def check_and_change_state_before_execution(
        self,
        verbose: bool = ...,
        ignore_all_deps: bool = ...,
        ignore_depends_on_past: bool = ...,
        wait_for_past_depends_before_skipping: bool = ...,
        ignore_task_deps: bool = ...,
        ignore_ti_state: bool = ...,
        mark_success: bool = ...,
        test_mode: bool = ...,
        job_id: str | None = ...,
        pool: str | None = ...,
        external_executor_id: str | None = ...,
        session: Session = ...,
    ) -> bool: ...
    def emit_state_change_metric(self, new_state: TaskInstanceState) -> None:
        """
        Send a time metric representing how much time a given state transition took.

        The previous state and metric name is deduced from the state the task was put in.

        :param new_state: The state that has just been set for this task.
            We do not use `self.state`, because sometimes the state is updated directly in the DB and not in
            the local TaskInstance object.
            Supported states: QUEUED and RUNNING
        """
        ...

    def clear_next_method_args(self) -> None:
        """Ensure we unset next_method and next_kwargs to ensure that any retries don't reuse them."""
        ...

    @provide_session
    def defer_task(
        self, exception: TaskDeferred | None, session: Session = ...
    ) -> None:
        """
        Mark the task as deferred and sets up the trigger that is needed to resume it when TaskDeferred is raised.

        :meta: private
        """
        ...

    @provide_session
    def run(
        self,
        verbose: bool = ...,
        ignore_all_deps: bool = ...,
        ignore_depends_on_past: bool = ...,
        wait_for_past_depends_before_skipping: bool = ...,
        ignore_task_deps: bool = ...,
        ignore_ti_state: bool = ...,
        mark_success: bool = ...,
        test_mode: bool = ...,
        job_id: str | None = ...,
        pool: str | None = ...,
        session: Session = ...,
        raise_on_defer: bool = ...,
    ) -> None:
        """Run TaskInstance."""
        ...

    def dry_run(self) -> None:
        """Only Renders Templates for the TI."""
        ...

    @staticmethod
    def get_truncated_error_traceback(
        error: BaseException, truncate_to: Callable
    ) -> TracebackType | None:
        """
        Truncate the traceback of an exception to the first frame called from within a given function.

        :param error: exception to get traceback from
        :param truncate_to: Function to truncate TB to. Must have a ``__code__`` attribute

        :meta private:
        """
        ...

    @classmethod
    def fetch_handle_failure_context(
        cls,
        ti: TaskInstance,
        error: None | str | BaseException,
        test_mode: bool | None = ...,
        context: Context | None = ...,
        force_fail: bool = ...,
        *,
        session: Session,
        fail_stop: bool = ...,
    ):  # -> dict[str, Any]:
        """
        Handle Failure for the TaskInstance.

        :param fail_stop: if true, stop remaining tasks in dag
        """
        ...

    @staticmethod
    @internal_api_call
    @provide_session
    def save_to_db(
        ti: TaskInstance | TaskInstancePydantic, session: Session = ...
    ):  # -> None:
        ...
    @provide_session
    def handle_failure(
        self,
        error: None | str | BaseException,
        test_mode: bool | None = ...,
        context: Context | None = ...,
        force_fail: bool = ...,
        session: Session = ...,
    ) -> None:
        """
        Handle Failure for a task instance.

        :param error: if specified, log the specific exception if thrown
        :param session: SQLAlchemy ORM Session
        :param test_mode: doesn't record success or failure in the DB if True
        :param context: Jinja2 context
        :param force_fail: if True, task does not retry
        """
        ...

    def is_eligible_to_retry(self):  # -> bool | Literal[0] | None:
        """Is task instance is eligible for retry."""
        ...

    def get_template_context(
        self, session: Session | None = ..., ignore_param_exceptions: bool = ...
    ) -> Context:
        """
        Return TI Context.

        :param session: SQLAlchemy ORM Session
        :param ignore_param_exceptions: flag to suppress value exceptions while initializing the ParamsDict
        """
        ...

    @provide_session
    def get_rendered_template_fields(self, session: Session = ...) -> None:
        """
        Update task with rendered template fields for presentation in UI.

        If task has already run, will fetch from DB; otherwise will render.
        """
        ...

    def overwrite_params_with_dag_run_conf(
        self, params: dict, dag_run: DagRun
    ):  # -> None:
        """Overwrite Task Params with DagRun.conf."""
        ...

    def render_templates(
        self, context: Context | None = ..., jinja_env: jinja2.Environment | None = ...
    ) -> Operator:
        """
        Render templates in the operator fields.

        If the task was originally mapped, this may replace ``self.task`` with
        the unmapped, fully rendered BaseOperator. The original ``self.task``
        before replacement is returned.
        """
        ...

    def render_k8s_pod_yaml(self) -> dict | None:
        """Render the k8s pod yaml."""
        ...

    @provide_session
    def get_rendered_k8s_spec(self, session: Session = ...):
        """Render the k8s pod yaml."""
        ...

    def get_email_subject_content(
        self, exception: BaseException, task: BaseOperator | None = ...
    ) -> tuple[str, str, str]:
        """
        Get the email subject content for exceptions.

        :param exception: the exception sent in the email
        :param task:
        """
        ...

    def email_alert(self, exception, task: BaseOperator) -> None:
        """
        Send alert email with exception information.

        :param exception: the exception
        :param task: task related to the exception
        """
        ...

    def set_duration(self) -> None:
        """Set task instance duration."""
        ...

    @provide_session
    def xcom_push(
        self,
        key: str,
        value: Any,
        execution_date: datetime | None = ...,
        session: Session = ...,
    ) -> None:
        """
        Make an XCom available for tasks to pull.

        :param key: Key to store the value under.
        :param value: Value to store. What types are possible depends on whether
            ``enable_xcom_pickling`` is true or not. If so, this can be any
            picklable object; only be JSON-serializable may be used otherwise.
        :param execution_date: Deprecated parameter that has no effect.
        """
        ...

    @provide_session
    def xcom_pull(
        self,
        task_ids: str | Iterable[str] | None = ...,
        dag_id: str | None = ...,
        key: str = ...,
        include_prior_dates: bool = ...,
        session: Session = ...,
        *,
        map_indexes: int | Iterable[int] | None = ...,
        default: Any = ...,
    ) -> Any:
        """
        Pull XComs that optionally meet certain criteria.

        :param key: A key for the XCom. If provided, only XComs with matching
            keys will be returned. The default key is ``'return_value'``, also
            available as constant ``XCOM_RETURN_KEY``. This key is automatically
            given to XComs returned by tasks (as opposed to being pushed
            manually). To remove the filter, pass *None*.
        :param task_ids: Only XComs from tasks with matching ids will be
            pulled. Pass *None* to remove the filter.
        :param dag_id: If provided, only pulls XComs from this DAG. If *None*
            (default), the DAG of the calling task is used.
        :param map_indexes: If provided, only pull XComs with matching indexes.
            If *None* (default), this is inferred from the task(s) being pulled
            (see below for details).
        :param include_prior_dates: If False, only XComs from the current
            execution_date are returned. If *True*, XComs from previous dates
            are returned as well.

        When pulling one single task (``task_id`` is *None* or a str) without
        specifying ``map_indexes``, the return value is inferred from whether
        the specified task is mapped. If not, value from the one single task
        instance is returned. If the task to pull is mapped, an iterator (not a
        list) yielding XComs from mapped task instances is returned. In either
        case, ``default`` (*None* if not specified) is returned if no matching
        XComs are found.

        When pulling multiple tasks (i.e. either ``task_id`` or ``map_index`` is
        a non-str iterable), a list of matching XComs is returned. Elements in
        the list is ordered by item ordering in ``task_id`` and ``map_index``.
        """
        ...

    @provide_session
    def get_num_running_task_instances(
        self, session: Session, same_dagrun: bool = ...
    ) -> int:
        """Return Number of running TIs from the DB."""
        ...

    def init_run_context(self, raw: bool = ...) -> None:
        """Set the log context."""
        ...

    @staticmethod
    def filter_for_tis(
        tis: Iterable[TaskInstance | TaskInstanceKey],
    ) -> BooleanClauseList | None:
        """Return SQLAlchemy filter to query selected task instances."""
        ...

    @classmethod
    def ti_selector_condition(
        cls, vals: Collection[str | tuple[str, int]]
    ) -> ColumnOperators:
        """
        Build an SQLAlchemy filter for a list of task_ids or tuples of (task_id,map_index).

        :meta private:
        """
        ...

    @provide_session
    def schedule_downstream_tasks(
        self, session: Session = ..., max_tis_per_query: int | None = ...
    ):  # -> None:
        """
        Schedule downstream tasks of this task instance.

        :meta: private
        """
        ...

    def get_relevant_upstream_map_indexes(
        self, upstream: Operator, ti_count: int | None, *, session: Session
    ) -> int | range | None:
        """
        Infer the map indexes of an upstream "relevant" to this ti.

        The bulk of the logic mainly exists to solve the problem described by
        the following example, where 'val' must resolve to different values,
        depending on where the reference is being used::

            @task
            def this_task(v):  # This is self.task.
                return v * 2

            @task_group
            def tg1(inp):
                val = upstream(inp)  # This is the upstream task.
                this_task(val)  # When inp is 1, val here should resolve to 2.
                return val

            # This val is the same object returned by tg1.
            val = tg1.expand(inp=[1, 2, 3])

            @task_group
            def tg2(inp):
                another_task(inp, val)  # val here should resolve to [2, 4, 6].

            tg2.expand(inp=["a", "b"])

        The surrounding mapped task groups of ``upstream`` and ``self.task`` are
        inspected to find a common "ancestor". If such an ancestor is found,
        we need to return specific map indexes to pull a partial value from
        upstream XCom.

        :param upstream: The referenced upstream task.
        :param ti_count: The total count of task instance this task was expanded
            by the scheduler, i.e. ``expanded_ti_count`` in the template context.
        :return: Specific map index or map indexes to pull, or ``None`` if we
            want to "whole" return value (i.e. no mapped task groups involved).
        """
        ...

    def clear_db_references(self, session: Session):  # -> None:
        """
        Clear db tables that have a reference to this instance.

        :param session: ORM Session

        :meta private:
        """
        ...

TaskInstanceStateType = tuple[TaskInstanceKey, TaskInstanceState]

class SimpleTaskInstance:
    """
    Simplified Task Instance.

    Used to send data between processes via Queues.
    """

    def __init__(
        self,
        dag_id: str,
        task_id: str,
        run_id: str,
        start_date: datetime | None,
        end_date: datetime | None,
        try_number: int,
        map_index: int,
        state: str,
        executor: str | None,
        executor_config: Any,
        pool: str,
        queue: str,
        key: TaskInstanceKey,
        run_as_user: str | None = ...,
        priority_weight: int | None = ...,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other) -> bool: ...
    def as_dict(self):  # -> dict[str, Any]:
        ...
    @classmethod
    def from_ti(cls, ti: TaskInstance) -> SimpleTaskInstance: ...
    @classmethod
    def from_dict(cls, obj_dict: dict) -> SimpleTaskInstance: ...

class TaskInstanceNote(TaskInstanceDependencies):
    """For storage of arbitrary notes concerning the task instance."""

    __tablename__ = ...
    user_id = ...
    task_id = ...
    dag_id = ...
    run_id = ...
    map_index = ...
    content = ...
    created_at = ...
    updated_at = ...
    task_instance = ...
    __table_args__ = ...
    def __init__(self, content, user_id=...) -> None: ...
    def __repr__(self):  # -> str:
        ...

STATICA_HACK = ...
if STATICA_HACK: ...
