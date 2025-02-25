"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, Any

from airflow.metrics.protocols import DeltaType, TimerProtocol
from airflow.typing_compat import Protocol

if TYPE_CHECKING: ...

class StatsLogger(Protocol):
    """This class is only used for TypeChecking (for IDEs, mypy, etc)."""

    instance: StatsLogger | NoStatsLogger | None = ...
    @classmethod
    def incr(
        cls,
        stat: str,
        count: int = ...,
        rate: int | float = ...,
        *,
        tags: dict[str, Any] | None = ...,
    ) -> None:
        """Increment stat."""
        ...

    @classmethod
    def decr(
        cls,
        stat: str,
        count: int = ...,
        rate: int | float = ...,
        *,
        tags: dict[str, Any] | None = ...,
    ) -> None:
        """Decrement stat."""
        ...

    @classmethod
    def gauge(
        cls,
        stat: str,
        value: float,
        rate: int | float = ...,
        delta: bool = ...,
        *,
        tags: dict[str, Any] | None = ...,
    ) -> None:
        """Gauge stat."""
        ...

    @classmethod
    def timing(
        cls, stat: str, dt: DeltaType | None, *, tags: dict[str, Any] | None = ...
    ) -> None:
        """Stats timing."""
        ...

    @classmethod
    def timer(cls, *args, **kwargs) -> TimerProtocol:
        """Timer metric that can be cancelled."""
        ...

class NoStatsLogger:
    """If no StatsLogger is configured, NoStatsLogger is used as a fallback."""

    @classmethod
    def incr(
        cls,
        stat: str,
        count: int = ...,
        rate: int = ...,
        *,
        tags: dict[str, str] | None = ...,
    ) -> None:
        """Increment stat."""
        ...

    @classmethod
    def decr(
        cls,
        stat: str,
        count: int = ...,
        rate: int = ...,
        *,
        tags: dict[str, str] | None = ...,
    ) -> None:
        """Decrement stat."""
        ...

    @classmethod
    def gauge(
        cls,
        stat: str,
        value: int,
        rate: int = ...,
        delta: bool = ...,
        *,
        tags: dict[str, str] | None = ...,
    ) -> None:
        """Gauge stat."""
        ...

    @classmethod
    def timing(
        cls, stat: str, dt: DeltaType, *, tags: dict[str, str] | None = ...
    ) -> None:
        """Stats timing."""
        ...

    @classmethod
    def timer(cls, *args, **kwargs) -> TimerProtocol:
        """Timer metric that can be cancelled."""
        ...
