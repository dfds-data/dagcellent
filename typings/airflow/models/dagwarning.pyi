"""
This type stub file was generated by pyright.
"""

from enum import Enum
from typing import TYPE_CHECKING

from airflow.api_internal.internal_api_call import internal_api_call
from airflow.models.base import Base
from airflow.utils.session import provide_session
from sqlalchemy.orm import Session

if TYPE_CHECKING: ...

class DagWarning(Base):
    """
    A table to store DAG warnings.

    DAG warnings are problems that don't rise to the level of failing the DAG parse
    but which users should nonetheless be warned about.  These warnings are recorded
    when parsing DAG and displayed on the Webserver in a flash message.
    """

    dag_id = ...
    warning_type = ...
    message = ...
    timestamp = ...
    __tablename__ = ...
    __table_args__ = ...
    def __init__(
        self, dag_id: str, error_type: str, message: str, **kwargs
    ) -> None: ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    @classmethod
    @internal_api_call
    @provide_session
    def purge_inactive_dag_warnings(cls, session: Session = ...) -> None:
        """
        Deactivate DagWarning records for inactive dags.

        :return: None
        """
        ...

class DagWarningType(str, Enum):
    """
    Enum for DAG warning types.

    This is the set of allowable values for the ``warning_type`` field
    in the DagWarning model.
    """

    NONEXISTENT_POOL = ...
