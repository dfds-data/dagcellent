"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

from airflow.callbacks.base_callback_sink import BaseCallbackSink
from airflow.callbacks.callback_requests import CallbackRequest
from airflow.utils.session import provide_session
from sqlalchemy.orm import Session

if TYPE_CHECKING: ...

class DatabaseCallbackSink(BaseCallbackSink):
    """Sends callbacks to database."""

    @provide_session
    def send(self, callback: CallbackRequest, session: Session = ...) -> None:
        """Send callback for execution."""
        ...
