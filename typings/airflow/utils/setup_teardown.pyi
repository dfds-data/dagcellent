"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

from airflow.models.abstractoperator import AbstractOperator
from airflow.models.taskmixin import DependencyMixin
from airflow.models.xcom_arg import PlainXComArg

if TYPE_CHECKING: ...

class BaseSetupTeardownContext:
    """
    Context manager for setup/teardown tasks.

    :meta private:
    """

    active: bool = ...
    context_map: dict[
        AbstractOperator | tuple[AbstractOperator], list[AbstractOperator]
    ] = ...
    _context_managed_setup_task: AbstractOperator | list[AbstractOperator] = ...
    _previous_context_managed_setup_task: list[
        AbstractOperator | list[AbstractOperator]
    ] = ...
    _context_managed_teardown_task: AbstractOperator | list[AbstractOperator] = ...
    _previous_context_managed_teardown_task: list[
        AbstractOperator | list[AbstractOperator]
    ] = ...
    _teardown_downstream_of_setup: AbstractOperator | list[AbstractOperator] = ...
    _previous_teardown_downstream_of_setup: list[
        AbstractOperator | list[AbstractOperator]
    ] = ...
    _setup_upstream_of_teardown: AbstractOperator | list[AbstractOperator] = ...
    _previous_setup_upstream_of_teardown: list[
        AbstractOperator | list[AbstractOperator]
    ] = ...
    @classmethod
    def push_context_managed_setup_task(
        cls, task: AbstractOperator | list[AbstractOperator]
    ):  # -> None:
        ...
    @classmethod
    def push_context_managed_teardown_task(
        cls, task: AbstractOperator | list[AbstractOperator]
    ):  # -> None:
        ...
    @classmethod
    def pop_context_managed_setup_task(
        cls,
    ) -> AbstractOperator | list[AbstractOperator]: ...
    @classmethod
    def pop_context_managed_teardown_task(
        cls,
    ) -> AbstractOperator | list[AbstractOperator]: ...
    @classmethod
    def pop_teardown_downstream_of_setup(
        cls,
    ) -> AbstractOperator | list[AbstractOperator]: ...
    @classmethod
    def pop_setup_upstream_of_teardown(
        cls,
    ) -> AbstractOperator | list[AbstractOperator]: ...
    @classmethod
    def set_dependency(
        cls,
        receiving_task: AbstractOperator | list[AbstractOperator],
        new_task: AbstractOperator | list[AbstractOperator],
        upstream=...,
    ):  # -> None:
        ...
    @classmethod
    def update_context_map(cls, task: DependencyMixin):  # -> None:
        ...
    @classmethod
    def push_setup_teardown_task(
        cls, operator: AbstractOperator | list[AbstractOperator]
    ):  # -> None:
        ...
    @classmethod
    def set_teardown_task_as_leaves(cls, leaves):  # -> None:
        ...
    @classmethod
    def set_setup_task_as_roots(cls, roots):  # -> None:
        ...
    @classmethod
    def set_work_task_roots_and_leaves(cls):  # -> None:
        """Set the work task roots and leaves."""
        ...

    @classmethod
    def set_setup_teardown_relationships(cls):  # -> None:
        """
        Set relationship between setup to setup and teardown to teardown.

        code:: python
            with setuptask >> teardowntask:
                with setuptask2 >> teardowntask2:
                    ...

        We set setuptask >> setuptask2, teardowntask >> teardowntask2
        """
        ...

    @classmethod
    def error(cls, message: str): ...

class SetupTeardownContext(BaseSetupTeardownContext):
    """Context manager for setup and teardown tasks."""

    @staticmethod
    def add_task(task: AbstractOperator | PlainXComArg):  # -> None:
        """Add task to context manager."""
        ...
