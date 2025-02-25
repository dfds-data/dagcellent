"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

from airflow.datasets import Dataset

if TYPE_CHECKING: ...
hookspec = ...

@hookspec
def on_dataset_created(dataset: Dataset):  # -> None:
    """Execute when a new dataset is created."""
    ...

@hookspec
def on_dataset_changed(dataset: Dataset):  # -> None:
    """Execute when dataset change is registered."""
    ...
