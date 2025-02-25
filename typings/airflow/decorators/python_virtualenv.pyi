"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING

from airflow.decorators.base import TaskDecorator
from airflow.decorators.python import _PythonDecoratedOperator
from airflow.operators.python import PythonVirtualenvOperator

if TYPE_CHECKING: ...

class _PythonVirtualenvDecoratedOperator(
    _PythonDecoratedOperator, PythonVirtualenvOperator
):
    """Wraps a Python callable and captures args/kwargs when called for execution."""

    template_fields = ...
    custom_operator_name: str = ...

def virtualenv_task(
    python_callable: Callable | None = ...,
    multiple_outputs: bool | None = ...,
    **kwargs,
) -> TaskDecorator:
    """
    Wrap a callable into an Airflow operator to run via a Python virtual environment.

    Accepts kwargs for operator kwarg. Can be reused in a single DAG.

    This function is only used only used during type checking or auto-completion.

    :meta private:

    :param python_callable: Function to decorate
    :param multiple_outputs: If set to True, the decorated function's return value will be unrolled to
        multiple XCom values. Dict will unroll to XCom values with its keys as XCom keys.
        Defaults to False.
    """
    ...
