"""
This type stub file was generated by pyright.
"""

from airflow.ti_deps.deps.base_ti_dep import BaseTIDep

"""Contains the TaskNotRunningDep."""

class TaskNotRunningDep(BaseTIDep):
    """Ensures that the task instance's state is not running."""

    NAME = ...
    IGNORABLE = ...
    def __eq__(self, other) -> bool:
        """Check if two task instance dependencies are of the same type."""
        ...

    def __hash__(self) -> int:
        """Compute the hash value based on the type of the task instance dependency."""
        ...
