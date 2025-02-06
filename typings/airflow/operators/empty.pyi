"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context

if TYPE_CHECKING: ...

class EmptyOperator(BaseOperator):
    """
    Operator that does literally nothing.

    It can be used to group tasks in a DAG.
    The task is evaluated by the scheduler but never processed by the executor.
    """

    ui_color = ...
    inherits_from_empty_operator = ...
    def execute(self, context: Context):  # -> None:
        ...
