"""
This type stub file was generated by pyright.
"""

from typing import ContextManager

from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.platform import IS_WINDOWS

_timeout = ContextManager[None]

class TimeoutWindows(_timeout, LoggingMixin):
    """Windows timeout version: To be used in a ``with`` block and timeout its content."""

    def __init__(self, seconds=..., error_message=...) -> None: ...
    def handle_timeout(self, *args):
        """Log information and raises AirflowTaskTimeout."""
        ...

    def __enter__(self):  # -> None:
        ...
    def __exit__(self, type_, value, traceback):  # -> None:
        ...

class TimeoutPosix(_timeout, LoggingMixin):
    """POSIX Timeout version: To be used in a ``with`` block and timeout its content."""

    def __init__(self, seconds=..., error_message=...) -> None: ...
    def handle_timeout(self, signum, frame):
        """Log information and raises AirflowTaskTimeout."""
        ...

    def __enter__(self):  # -> None:
        ...
    def __exit__(self, type_, value, traceback):  # -> None:
        ...

if IS_WINDOWS:
    timeout: type[TimeoutWindows | TimeoutPosix] = ...
else:
    timeout = ...
