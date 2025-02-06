"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING

from airflow.decorators.base import TaskDecorator
from airflow.decorators.python import _PythonDecoratedOperator
from airflow.operators.python import BranchExternalPythonOperator

if TYPE_CHECKING: ...

class _BranchExternalPythonDecoratedOperator(
    _PythonDecoratedOperator, BranchExternalPythonOperator
):
    """Wraps a Python callable and captures args/kwargs when called for execution."""

    template_fields = ...
    custom_operator_name: str = ...

def branch_external_python_task(
    python_callable: Callable | None = ...,
    multiple_outputs: bool | None = ...,
    **kwargs,
) -> TaskDecorator:
    """
    Wrap a python function into a BranchExternalPythonOperator.

    For more information on how to use this operator, take a look at the guide:
    :ref:`concepts:branching`

    Accepts kwargs for operator kwarg. Can be reused in a single DAG.

    :param python_callable: Function to decorate
    :param multiple_outputs: if set, function return value will be
        unrolled to multiple XCom values. Dict will unroll to xcom values with keys as XCom keys.
        Defaults to False.
    """
    ...
