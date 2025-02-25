"""
This type stub file was generated by pyright.
"""

import contextlib
from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

if TYPE_CHECKING: ...
__current_task_instance_session: Session | None = ...
log = ...

def get_current_task_instance_session() -> Session: ...
@contextlib.contextmanager
def set_current_task_instance_session(
    session: Session,
):  # -> Generator[None, Any, None]:
    ...
