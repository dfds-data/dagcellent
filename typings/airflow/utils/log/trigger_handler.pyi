"""
This type stub file was generated by pyright.
"""

import logging
from contextvars import ContextVar
from logging.handlers import QueueHandler
from typing import TYPE_CHECKING

from airflow.utils.log.file_task_handler import FileTaskHandler

if TYPE_CHECKING: ...
ctx_task_instance: ContextVar = ...
ctx_trigger_id: ContextVar = ...
ctx_trigger_end: ContextVar = ...
ctx_indiv_trigger: ContextVar = ...

class TriggerMetadataFilter(logging.Filter):
    """
    Injects TI key, triggerer job_id, and trigger_id into the log record.

    :meta private:
    """

    def filter(self, record):  # -> Literal[True]:
        ...

class DropTriggerLogsFilter(logging.Filter):
    """
    If record has attr with name ctx_indiv_trigger, filter the record.

    The purpose here is to prevent trigger logs from going to stdout
    in the trigger service.

    :meta private:
    """

    def filter(self, record):  # -> bool:
        ...

class TriggererHandlerWrapper(logging.Handler):
    """
    Wrap inheritors of FileTaskHandler and direct log messages to them based on trigger_id.

    :meta private:
    """

    trigger_should_queue = ...
    def __init__(self, base_handler: FileTaskHandler, level=...) -> None: ...
    def emit(self, record):  # -> None:
        ...
    def handle(self, record):  # -> LogRecord | bool:
        ...
    def close_one(self, trigger_id):  # -> None:
        ...
    def flush(self):  # -> None:
        ...
    def close(self):  # -> None:
        ...

class LocalQueueHandler(QueueHandler):
    """
    Send messages to queue.

    :meta private:
    """

    def emit(self, record: logging.LogRecord) -> None: ...
