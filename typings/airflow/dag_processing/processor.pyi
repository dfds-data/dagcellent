"""
This type stub file was generated by pyright.
"""

import logging
from collections.abc import Generator, Iterable
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from airflow.api_internal.internal_api_call import internal_api_call
from airflow.callbacks.callback_requests import CallbackRequest
from airflow.models.dag import DAG
from airflow.models.dagbag import DagBag
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.mixins import MultiprocessingStartMethodMixin
from airflow.utils.session import provide_session
from sqlalchemy.orm.session import Session

if TYPE_CHECKING: ...

@dataclass
class _QueryCounter:
    queries_number: int = ...
    def inc(self):  # -> None:
        ...

@contextmanager
def count_queries(session: Session) -> Generator[_QueryCounter, None, None]: ...

class DagFileProcessorProcess(LoggingMixin, MultiprocessingStartMethodMixin):
    """
    Runs DAG processing in a separate process using DagFileProcessor.

    :param file_path: a Python file containing Airflow DAG definitions
    :param pickle_dags: whether to serialize the DAG objects to the DB
    :param dag_ids: If specified, only look at these DAG ID's
    :param callback_requests: failure callback to execute
    """

    class_creation_counter = ...
    def __init__(
        self,
        file_path: str,
        pickle_dags: bool,
        dag_ids: list[str] | None,
        dag_directory: str,
        callback_requests: list[CallbackRequest],
    ) -> None: ...
    @property
    def file_path(self) -> str: ...
    def start(self) -> None:
        """Launch the process and start processing the DAG."""
        ...

    def kill(self) -> None:
        """Kill the process launched to process the file, and ensure consistent state."""
        ...

    def terminate(self, sigkill: bool = ...) -> None:
        """
        Terminate (and then kill) the process launched to process the file.

        :param sigkill: whether to issue a SIGKILL if SIGTERM doesn't work.
        """
        ...

    @property
    def pid(self) -> int:
        """PID of the process launched to process the given file."""
        ...

    @property
    def exit_code(self) -> int | None:
        """
        After the process is finished, this can be called to get the return code.

        :return: the exit code of the process
        """
        ...

    @property
    def done(self) -> bool:
        """
        Check if the process launched to process this file is done.

        :return: whether the process is finished running
        """
        ...

    @property
    def result(self) -> tuple[int, int, int] | None:
        """Result of running ``DagFileProcessor.process_file()``."""
        ...

    @property
    def start_time(self) -> datetime:
        """Time when this started to process the file."""
        ...

    @property
    def waitable_handle(self): ...
    def import_modules(self, file_path: str | Iterable[str]):  # -> None:
        ...

class DagFileProcessor(LoggingMixin):
    """
    Process a Python file containing Airflow DAGs.

    This includes:

    1. Execute the file and look for DAG objects in the namespace.
    2. Execute any Callbacks if passed to DagFileProcessor.process_file
    3. Serialize the DAGs and save it to DB (or update existing record in the DB).
    4. Pickle the DAG and save it to the DB (if necessary).
    5. Record any errors importing the file into ORM

    Returns a tuple of 'number of dags found' and 'the count of import errors'

    :param dag_ids: If specified, only look at these DAG ID's
    :param log: Logger to save the processing process
    """

    UNIT_TEST_MODE: bool = ...
    def __init__(
        self, dag_ids: list[str] | None, dag_directory: str, log: logging.Logger
    ) -> None: ...
    @classmethod
    @internal_api_call
    @provide_session
    def manage_slas(cls, dag_folder, dag_id: str, session: Session = ...) -> None:
        """
        Find all tasks that have SLAs defined, and send alert emails when needed.

        New SLA misses are also recorded in the database.

        We are assuming that the scheduler runs often, so we only check for
        tasks that should have succeeded in the past hour.
        """
        ...

    @staticmethod
    @internal_api_call
    @provide_session
    def update_import_errors(
        file_last_changed: dict[str, datetime],
        import_errors: dict[str, str],
        processor_subdir: str | None,
        session: Session = ...,
    ) -> None:
        """
        Update any import errors to be displayed in the UI.

        For the DAGs in the given DagBag, record any associated import errors and clears
        errors for files that no longer have them. These are usually displayed through the
        Airflow UI so that users know that there are issues parsing DAGs.
        :param file_last_changed: Dictionary containing the last changed time of the files
        :param import_errors: Dictionary containing the import errors
        :param session: session for ORM operations
        """
        ...

    @classmethod
    def update_dag_warnings(cla, *, dagbag: DagBag) -> None:
        """Validate and raise exception if any task in a dag is using a non-existent pool."""
        ...

    @classmethod
    @internal_api_call
    @provide_session
    def execute_callbacks(
        cls,
        dagbag: DagBag,
        callback_requests: list[CallbackRequest],
        unit_test_mode: bool,
        session: Session = ...,
    ) -> None:
        """
        Execute on failure callbacks.

        These objects can come from SchedulerJobRunner or from DagProcessorJobRunner.

        :param dagbag: Dag Bag of dags
        :param callback_requests: failure callbacks to execute
        :param session: DB session.

        :return: number of queries executed
        """
        ...

    @classmethod
    @internal_api_call
    @provide_session
    def execute_callbacks_without_dag(
        cls,
        callback_requests: list[CallbackRequest],
        unit_test_mode: bool,
        session: Session = ...,
    ) -> None:
        """
        Execute what callbacks we can as "best effort" when the dag cannot be found/had parse errors.

        This is so important so that tasks that failed when there is a parse
        error don't get stuck in queued state.
        """
        ...

    @provide_session
    def process_file(
        self,
        file_path: str,
        callback_requests: list[CallbackRequest],
        pickle_dags: bool = ...,
        session: Session = ...,
    ) -> tuple[int, int, int]:
        """
        Process a Python file containing Airflow DAGs.

        This includes:

        1. Execute the file and look for DAG objects in the namespace.
        2. Execute any Callbacks if passed to this method.
        3. Serialize the DAGs and save it to DB (or update existing record in the DB).
        4. Pickle the DAG and save it to the DB (if necessary).
        5. Mark any DAGs which are no longer present as inactive
        6. Record any errors importing the file into ORM

        :param file_path: the path to the Python file that should be executed
        :param callback_requests: failure callback to execute
        :param pickle_dags: whether serialize the DAGs found in the file and
            save them to the db
        :return: number of dags found, count of import errors, last number of db queries
        """
        ...

    @staticmethod
    @internal_api_call
    @provide_session
    def save_dag_to_db(
        dags: dict[str, DAG], dag_directory: str, pickle_dags: bool = ..., session=...
    ):  # -> dict[Any, Any]:
        ...
