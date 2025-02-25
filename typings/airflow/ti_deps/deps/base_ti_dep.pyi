"""
This type stub file was generated by pyright.
"""

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, NamedTuple

from airflow.models.taskinstance import TaskInstance
from airflow.ti_deps.dep_context import DepContext
from airflow.utils.session import provide_session
from sqlalchemy.orm import Session

if TYPE_CHECKING: ...

class BaseTIDep:
    """
    Abstract base class for task instances dependencies.

    All dependencies must be satisfied in order for task instances to run.
    For example, a task that can only run if a certain number of its upstream tasks succeed.
    This is an abstract class and must be subclassed to be used.
    """

    IGNORABLE = ...
    IS_TASK_DEP = ...
    def __eq__(self, other: Any) -> bool:
        """Check if two task instance dependencies are equal by comparing their types."""
        ...

    def __hash__(self) -> int:
        """Compute the hash value based on the task instance dependency type."""
        ...

    def __repr__(self) -> str:
        """Return a string representation of the task instance dependency."""
        ...

    @property
    def name(self) -> str:
        """
        The human-readable name for the dependency.

        Use the class name as the default if ``NAME`` is not provided.
        """
        ...

    @provide_session
    def get_dep_statuses(
        self, ti: TaskInstance, session: Session, dep_context: DepContext | None = ...
    ) -> Iterator[TIDepStatus]:
        """
        Wrap around the private _get_dep_statuses method.

        Contains some global checks for all dependencies.

        :param ti: the task instance to get the dependency status for
        :param session: database session
        :param dep_context: the context for which this dependency should be evaluated for
        """
        ...

    @provide_session
    def is_met(
        self, ti: TaskInstance, session: Session, dep_context: DepContext | None = ...
    ) -> bool:
        """
        Return whether a dependency is met for a given task instance.

        A dependency is considered met if all the dependency statuses it reports are passing.

        :param ti: the task instance to see if this dependency is met for
        :param session: database session
        :param dep_context: The context this dependency is being checked under that stores
            state that can be used by this dependency.
        """
        ...

    @provide_session
    def get_failure_reasons(
        self, ti: TaskInstance, session: Session, dep_context: DepContext | None = ...
    ) -> Iterator[str]:
        """
        Return an iterable of strings that explain why this dependency wasn't met.

        :param ti: the task instance to see if this dependency is met for
        :param session: database session
        :param dep_context: The context this dependency is being checked under that stores
            state that can be used by this dependency.
        """
        ...

class TIDepStatus(NamedTuple):
    """Dependency status for a task instance indicating whether the task instance passed the dependency."""

    dep_name: str
    passed: bool
    reason: str
    ...
