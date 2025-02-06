"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeAlias, TypeVar

from airflow.decorators.base import Task, _TaskDecorator
from airflow.models.baseoperator import TaskPreExecuteHook
from airflow.utils.context import Context

if TYPE_CHECKING:
    BoolConditionFunc: TypeAlias = Callable[[Context], bool]
    MsgConditionFunc: TypeAlias = "Callable[[Context], tuple[bool, str | None]]"
    AnyConditionFunc: TypeAlias = "BoolConditionFunc | MsgConditionFunc"
__all__ = ["run_if", "skip_if"]
_T = TypeVar("_T", bound="Task[..., Any] | _TaskDecorator[..., Any, Any]")

def run_if(
    condition: AnyConditionFunc, skip_message: str | None = ...
) -> Callable[[_T], _T]:
    """
    Decorate a task to run only if a condition is met.

    :param condition: A function that takes a context and returns a boolean.
    :param skip_message: The message to log if the task is skipped.
        If None, a default message is used.
    """
    ...

def skip_if(
    condition: AnyConditionFunc, skip_message: str | None = ...
) -> Callable[[_T], _T]:
    """
    Decorate a task to skip if a condition is met.

    :param condition: A function that takes a context and returns a boolean.
    :param skip_message: The message to log if the task is skipped.
        If None, a default message is used.
    """
    ...

def wrap_skip(
    func: AnyConditionFunc, error_msg: str, *, reverse: bool
) -> TaskPreExecuteHook: ...
def combine_hooks(*hooks: TaskPreExecuteHook | None) -> TaskPreExecuteHook: ...
