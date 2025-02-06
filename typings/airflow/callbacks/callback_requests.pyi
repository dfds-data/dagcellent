"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

from airflow.models.taskinstance import SimpleTaskInstance
from airflow.utils.state import TaskInstanceState

if TYPE_CHECKING: ...

class CallbackRequest:
    """
    Base Class with information about the callback to be executed.

    :param full_filepath: File Path to use to run the callback
    :param msg: Additional Message that can be used for logging
    :param processor_subdir: Directory used by Dag Processor when parsed the dag.
    """

    def __init__(
        self,
        full_filepath: str,
        processor_subdir: str | None = ...,
        msg: str | None = ...,
    ) -> None: ...
    def __eq__(self, other) -> bool: ...
    def __repr__(self):  # -> str:
        ...
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json_str: str):  # -> Self:
        ...

class TaskCallbackRequest(CallbackRequest):
    """
    Task callback status information.

    A Class with information about the success/failure TI callback to be executed. Currently, only failure
    callbacks (when tasks are externally killed) and Zombies are run via DagFileProcessorProcess.

    :param full_filepath: File Path to use to run the callback
    :param simple_task_instance: Simplified Task Instance representation
    :param msg: Additional Message that can be used for logging to determine failure/zombie
    :param processor_subdir: Directory used by Dag Processor when parsed the dag.
    :param task_callback_type: e.g. whether on success, on failure, on retry.
    """

    def __init__(
        self,
        full_filepath: str,
        simple_task_instance: SimpleTaskInstance,
        processor_subdir: str | None = ...,
        msg: str | None = ...,
        task_callback_type: TaskInstanceState | None = ...,
    ) -> None: ...
    @property
    def is_failure_callback(self) -> bool:
        """Returns True if the callback is a failure callback."""
        ...

    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json_str: str):  # -> Self:
        ...

class DagCallbackRequest(CallbackRequest):
    """
    A Class with information about the success/failure DAG callback to be executed.

    :param full_filepath: File Path to use to run the callback
    :param dag_id: DAG ID
    :param run_id: Run ID for the DagRun
    :param processor_subdir: Directory used by Dag Processor when parsed the dag.
    :param is_failure_callback: Flag to determine whether it is a Failure Callback or Success Callback
    :param msg: Additional Message that can be used for logging
    """

    def __init__(
        self,
        full_filepath: str,
        dag_id: str,
        run_id: str,
        processor_subdir: str | None,
        is_failure_callback: bool | None = ...,
        msg: str | None = ...,
    ) -> None: ...

class SlaCallbackRequest(CallbackRequest):
    """
    A class with information about the SLA callback to be executed.

    :param full_filepath: File Path to use to run the callback
    :param dag_id: DAG ID
    :param processor_subdir: Directory used by Dag Processor when parsed the dag.
    """

    def __init__(
        self,
        full_filepath: str,
        dag_id: str,
        processor_subdir: str | None,
        msg: str | None = ...,
    ) -> None: ...
