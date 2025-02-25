"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, Any

from sqlalchemy import String

SQL_ALCHEMY_SCHEMA = ...
naming_convention = ...
metadata = ...
mapper_registry = ...
_sentinel = ...
if TYPE_CHECKING:
    Base = Any
else: ...
ID_LEN = ...

def get_id_collation_args():  # -> dict[str, str] | dict[Any, Any]:
    """Get SQLAlchemy args to use for COLLATION."""
    ...

COLLATION_ARGS: dict[str, Any] = ...

def StringID(*, length=..., **kwargs) -> String: ...

class TaskInstanceDependencies(Base):
    """Base class for depending models linked to TaskInstance."""

    __abstract__ = ...
    task_id = ...
    dag_id = ...
    run_id = ...
    map_index = ...
