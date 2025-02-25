"""
This type stub file was generated by pyright.
"""

import contextlib
import enum
from collections.abc import Generator, Iterable, Iterator, Sequence
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    TypeVar,
    overload,
)

import attrs
from airflow.models.connection import Connection
from airflow.typing_compat import Self
from airflow.utils.session import provide_session
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.selectable import Select

if TYPE_CHECKING:
    class MappedClassProtocol(Protocol):
        """Protocol for SQLALchemy model base."""

        __tablename__: str
        ...

T = TypeVar("T")
log = ...
_REVISION_HEADS_MAP = ...

@provide_session
def merge_conn(conn: Connection, session: Session = ...):  # -> None:
    """Add new Connection."""
    ...

@provide_session
def add_default_pool_if_not_exists(session: Session = ...):  # -> None:
    """Add default pool if it does not exist."""
    ...

@provide_session
def create_default_connections(session: Session = ...):  # -> None:
    """Create default Airflow connections."""
    ...

@provide_session
def initdb(
    session: Session = ...,
    load_connections: bool = ...,
    use_migration_files: bool = ...,
):  # -> None:
    """Initialize Airflow database."""
    ...

def check_migrations(timeout):  # -> None:
    """
    Wait for all airflow migrations to complete.

    :param timeout: Timeout for the migration in seconds
    :return: None
    """
    ...

def check_and_run_migrations():  # -> None:
    """Check and run migrations if necessary. Only use in a tty."""
    ...

@provide_session
def synchronize_log_template(*, session: Session = ...) -> None:
    """
    Synchronize log template configs with table.

    This checks if the last row fully matches the current config values, and
    insert a new row if not.
    """
    ...

def check_conn_id_duplicates(session: Session) -> Iterable[str]:
    """
    Check unique conn_id in connection table.

    :param session:  session of the sqlalchemy
    """
    ...

def check_username_duplicates(session: Session) -> Iterable[str]:
    """
    Check unique username in User & RegisterUser table.

    :param session:  session of the sqlalchemy
    :rtype: str
    """
    ...

def reflect_tables(
    tables: list[MappedClassProtocol | str] | None, session
):  # -> MetaData:
    """
    When running checks prior to upgrades, we use reflection to determine current state of the database.

    This function gets the current state of each table in the set of models
    provided and returns a SqlAlchemy metadata object containing them.
    """
    ...

def check_table_for_duplicates(
    *, session: Session, table_name: str, uniqueness: list[str], version: str
) -> Iterable[str]:
    """
    Check table for duplicates, given a list of columns which define the uniqueness of the table.

    Usage example:

    .. code-block:: python

        def check_task_fail_for_duplicates(session):
            from airflow.models.taskfail import TaskFail

            metadata = reflect_tables([TaskFail], session)
            task_fail = metadata.tables.get(TaskFail.__tablename__)  # type: ignore
            if task_fail is None:  # table not there
                return
            if "run_id" in task_fail.columns:  # upgrade already applied
                return
            yield from check_table_for_duplicates(
                table_name=task_fail.name,
                uniqueness=["dag_id", "task_id", "execution_date"],
                session=session,
                version="2.3",
            )

    :param table_name: table name to check
    :param uniqueness: uniqueness constraint to evaluate against
    :param session:  session of the sqlalchemy
    """
    ...

def check_conn_type_null(session: Session) -> Iterable[str]:
    """
    Check nullable conn_type column in Connection table.

    :param session:  session of the sqlalchemy
    """
    ...

def check_run_id_null(session: Session) -> Iterable[str]: ...
def check_bad_references(session: Session) -> Iterable[str]:
    """
    Go through each table and look for records that can't be mapped to a dag run.

    When we find such "dangling" rows we back them up in a special table and delete them
    from the main table.

    Starting in Airflow 2.2, we began a process of replacing `execution_date` with `run_id` in many tables.
    """
    @dataclass
    class BadReferenceConfig:
        """
        Bad reference config class.

        :param bad_rows_func: function that returns subquery which determines whether bad rows exist
        :param join_tables: table objects referenced in subquery
        :param ref_table: information-only identifier for categorizing the missing ref
        """

        ...

def print_happy_cat(message):  # -> None:
    ...
@provide_session
def upgradedb(
    *,
    to_revision: str | None = ...,
    from_revision: str | None = ...,
    show_sql_only: bool = ...,
    reserialize_dags: bool = ...,
    session: Session = ...,
    use_migration_files: bool = ...,
):  # -> None:
    """
    Upgrades the DB.

    :param to_revision: Optional Alembic revision ID to upgrade *to*.
        If omitted, upgrades to latest revision.
    :param from_revision: Optional Alembic revision ID to upgrade *from*.
        Not compatible with ``sql_only=False``.
    :param show_sql_only: if True, migration statements will be printed but not executed.
    :param session: sqlalchemy session with connection to Airflow metadata database
    :return: None
    """
    ...

@provide_session
def resetdb(
    session: Session = ..., skip_init: bool = ..., use_migration_files: bool = ...
):  # -> None:
    """Clear out the database."""
    ...

@provide_session
def bootstrap_dagbag(session: Session = ...):  # -> None:
    ...
@provide_session
def downgrade(
    *, to_revision, from_revision=..., show_sql_only=..., session: Session = ...
):  # -> None:
    """
    Downgrade the airflow metastore schema to a prior version.

    :param to_revision: The alembic revision to downgrade *to*.
    :param show_sql_only: if True, print sql statements but do not run them
    :param from_revision: if supplied, alembic revision to dawngrade *from*. This may only
        be used in conjunction with ``sql=True`` because if we actually run the commands,
        we should only downgrade from the *current* revision.
    :param session: sqlalchemy session for connection to airflow metadata database
    """
    ...

def drop_airflow_models(connection):  # -> None:
    """
    Drop all airflow models.

    :param connection: SQLAlchemy Connection
    :return: None
    """
    ...

def drop_airflow_moved_tables(connection):  # -> None:
    ...
@provide_session
def check(session: Session = ...):  # -> None:
    """
    Check if the database works.

    :param session: session of the sqlalchemy
    """
    ...
@enum.unique
class DBLocks(enum.IntEnum):
    """
    Cross-db Identifiers for advisory global database locks.

    Postgres uses int64 lock ids so we use the integer value, MySQL uses names, so we
    call ``str()`, which is implemented using the ``_name_`` field.
    """

    MIGRATIONS = ...
    SCHEDULER_CRITICAL_SECTION = ...
    def __str__(self) -> str: ...

@contextlib.contextmanager
def create_global_lock(
    session: Session, lock: DBLocks, lock_timeout: int = ...
) -> Generator[None, None, None]:
    """Contextmanager that will create and teardown a global db lock."""
    ...

def compare_type(
    context, inspected_column, metadata_column, inspected_type, metadata_type
):  # -> bool | None:
    """
    Compare types between ORM and DB .

    return False if the metadata_type is the same as the inspected_type
    or None to allow the default implementation to compare these
    types. a return value of True means the two types do not
    match and should result in a type change operation.
    """
    ...

def compare_server_default(
    context,
    inspected_column,
    metadata_column,
    inspected_default,
    metadata_default,
    rendered_metadata_default,
):  # -> Literal[False] | None:
    """
    Compare server defaults between ORM and DB .

    return True if the defaults are different, False if not, or None to allow the default implementation
    to compare these defaults

    In SQLite: task_instance.map_index & task_reschedule.map_index
    are not comparing accurately. Sometimes they are equal, sometimes they are not.
    Alembic warned that this feature has varied accuracy depending on backends.
    See: (https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.
        environment.EnvironmentContext.configure.params.compare_server_default)
    """
    ...

def get_sqla_model_classes():  # -> list[Any]:
    """
    Get all SQLAlchemy class mappers.

    SQLAlchemy < 1.4 does not support registry.mappers so we use
    try/except to handle it.
    """
    ...

def get_query_count(query_stmt: Select, *, session: Session) -> int:
    """
    Get count of a query.

    A SELECT COUNT() FROM is issued against the subquery built from the
    given statement. The ORDER BY clause is stripped from the statement
    since it's unnecessary for COUNT, and can impact query planning and
    degrade performance.

    :meta private:
    """
    ...

def check_query_exists(query_stmt: Select, *, session: Session) -> bool:
    """
    Check whether there is at least one row matching a query.

    A SELECT 1 FROM is issued against the subquery built from the given
    statement. The ORDER BY clause is stripped from the statement since it's
    unnecessary, and can impact query planning and degrade performance.

    :meta private:
    """
    ...

def exists_query(*where: ClauseElement, session: Session) -> bool:
    """
    Check whether there is at least one row matching given clauses.

    This does a SELECT 1 WHERE ... LIMIT 1 and check the result.

    :meta private:
    """
    ...
@attrs.define(slots=True)
class LazySelectSequence(Sequence[T]):
    """
    List-like interface to lazily access a database model query.

    The intended use case is inside a task execution context, where we manage an
    active SQLAlchemy session in the background.

    This is an abstract base class. Each use case should subclass, and implement
    the following static methods:

    * ``_rebuild_select`` is called when a lazy sequence is unpickled. Since it
      is not easy to pickle SQLAlchemy constructs, this class serializes the
      SELECT statements into plain text to storage. This method is called on
      deserialization to convert the textual clause back into an ORM SELECT.
    * ``_process_row`` is called when an item is accessed. The lazy sequence
      uses ``session.execute()`` to fetch rows from the database, and this
      method should know how to process each row into a value.

    :meta private:
    """

    _select_asc: ClauseElement
    _select_desc: ClauseElement
    _session: Session = ...
    _len: int | None = ...
    @classmethod
    def from_select(
        cls,
        select: Select,
        *,
        order_by: Sequence[ClauseElement],
        session: Session | None = ...,
    ) -> Self: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __getstate__(self) -> Any: ...
    def __setstate__(self, state: Any) -> None: ...
    def __bool__(self) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __reversed__(self) -> Iterator[T]: ...
    def __iter__(self) -> Iterator[T]: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, key: int) -> T: ...
    @overload
    def __getitem__(self, key: slice) -> Sequence[T]: ...
    def __getitem__(self, key: int | slice) -> T | Sequence[T]: ...
