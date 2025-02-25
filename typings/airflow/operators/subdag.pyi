"""
This type stub file was generated by pyright.
"""

from enum import Enum
from typing import TYPE_CHECKING

from airflow.models.dag import DAG
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.context import Context
from airflow.utils.session import provide_session
from sqlalchemy.orm.session import Session

"""
This module is deprecated. Please use :mod:`airflow.utils.task_group`.

The module which provides a way to nest your DAGs and so your levels of complexity.
"""
if TYPE_CHECKING: ...

class SkippedStatePropagationOptions(Enum):
    """Available options for skipped state propagation of subdag's tasks to parent dag tasks."""

    ALL_LEAVES = ...
    ANY_LEAF = ...

class SubDagOperator(BaseSensorOperator):
    """
    This class is deprecated, please use :class:`airflow.utils.task_group.TaskGroup`.

    This runs a sub dag. By convention, a sub dag's dag_id
    should be prefixed by its parent and a dot. As in `parent.child`.
    Although SubDagOperator can occupy a pool/concurrency slot,
    user can specify the mode=reschedule so that the slot will be
    released periodically to avoid potential deadlock.

    :param subdag: the DAG object to run as a subdag of the current DAG.
    :param session: sqlalchemy session
    :param conf: Configuration for the subdag
    :param propagate_skipped_state: by setting this argument you can define
        whether the skipped state of leaf task(s) should be propagated to the
        parent dag's downstream task.
    """

    ui_color = ...
    ui_fgcolor = ...
    subdag: DAG
    @provide_session
    def __init__(
        self,
        *,
        subdag: DAG,
        session: Session = ...,
        conf: dict | None = ...,
        propagate_skipped_state: SkippedStatePropagationOptions | None = ...,
        **kwargs,
    ) -> None: ...
    def pre_execute(self, context):  # -> None:
        ...
    def poke(self, context: Context): ...
    def post_execute(self, context, result=...):  # -> None:
        ...
