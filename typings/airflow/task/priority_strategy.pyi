"""
This type stub file was generated by pyright.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from airflow.models.taskinstance import TaskInstance

"""Priority weight strategies for task scheduling."""
if TYPE_CHECKING: ...

class PriorityWeightStrategy(ABC):
    """
    Priority weight strategy interface.

    This feature is experimental and subject to change at any time.

    Currently, we don't serialize the priority weight strategy parameters. This means that
    the priority weight strategy must be stateless, but you can add class attributes, and
    create multiple subclasses with different attributes values if you need to create
    different versions of the same strategy.
    """

    @abstractmethod
    def get_weight(self, ti: TaskInstance):  # -> None:
        """Get the priority weight of a task."""
        ...

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> PriorityWeightStrategy:
        """
        Deserialize a priority weight strategy from data.

        This is called when a serialized DAG is deserialized. ``data`` will be whatever
        was returned by ``serialize`` during DAG serialization. The default
        implementation constructs the priority weight strategy without any arguments.
        """
        ...

    def serialize(self) -> dict[str, Any]:
        """
        Serialize the priority weight strategy for JSON encoding.

        This is called during DAG serialization to store priority weight strategy information
        in the database. This should return a JSON-serializable dict that will be fed into
        ``deserialize`` when the DAG is deserialized. The default implementation returns
        an empty dict.
        """
        ...

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        ...

class _AbsolutePriorityWeightStrategy(PriorityWeightStrategy):
    """Priority weight strategy that uses the task's priority weight directly."""

    def get_weight(self, ti: TaskInstance):  # -> int:
        ...

class _DownstreamPriorityWeightStrategy(PriorityWeightStrategy):
    """Priority weight strategy that uses the sum of the priority weights of all downstream tasks."""

    def get_weight(self, ti: TaskInstance) -> int: ...

class _UpstreamPriorityWeightStrategy(PriorityWeightStrategy):
    """Priority weight strategy that uses the sum of the priority weights of all upstream tasks."""

    def get_weight(self, ti: TaskInstance):  # -> int:
        ...

airflow_priority_weight_strategies: dict[str, type[PriorityWeightStrategy]] = ...
airflow_priority_weight_strategies_classes = ...

def validate_and_load_priority_weight_strategy(
    priority_weight_strategy: str | PriorityWeightStrategy | None,
) -> PriorityWeightStrategy:
    """
    Validate and load a priority weight strategy.

    Returns the priority weight strategy if it is valid, otherwise raises an exception.

    :param priority_weight_strategy: The priority weight strategy to validate and load.

    :meta private:
    """
    ...
