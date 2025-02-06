"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, Union

import attr
from airflow.datasets import Dataset
from airflow.hooks.base import BaseHook
from airflow.io.path import ObjectStoragePath
from airflow.utils.log.logging_mixin import LoggingMixin

if TYPE_CHECKING:
    LineageContext = Union[BaseHook, ObjectStoragePath]
_hook_lineage_collector: HookLineageCollector | None = ...

@attr.define
class DatasetLineageInfo:
    """
    Holds lineage information for a single dataset.

    This class represents the lineage information for a single dataset, including the dataset itself,
    the count of how many times it has been encountered, and the context in which it was encountered.
    """

    dataset: Dataset
    count: int
    context: LineageContext
    ...

@attr.define
class HookLineage:
    """
    Holds lineage collected by HookLineageCollector.

    This class represents the lineage information collected by the `HookLineageCollector`. It stores
    the input and output datasets, each with an associated count indicating how many times the dataset
    has been encountered during the hook execution.
    """

    inputs: list[DatasetLineageInfo] = ...
    outputs: list[DatasetLineageInfo] = ...

class HookLineageCollector(LoggingMixin):
    """
    HookLineageCollector is a base class for collecting hook lineage information.

    It is used to collect the input and output datasets of a hook execution.
    """

    def __init__(self, **kwargs) -> None: ...
    def create_dataset(
        self,
        scheme: str | None,
        uri: str | None,
        dataset_kwargs: dict | None,
        dataset_extra: dict | None,
    ) -> Dataset | None:
        """
        Create a Dataset instance using the provided parameters.

        This method attempts to create a Dataset instance using the given parameters.
        It first checks if a URI is provided and falls back to using the default dataset factory
        with the given URI if no other information is available.

        If a scheme is provided but no URI, it attempts to find a dataset factory that matches
        the given scheme. If no such factory is found, it logs an error message and returns None.

        If dataset_kwargs is provided, it is used to pass additional parameters to the Dataset
        factory. The dataset_extra parameter is also passed to the factory as an ``extra`` parameter.
        """
        ...

    def add_input_dataset(
        self,
        context: LineageContext,
        scheme: str | None = ...,
        uri: str | None = ...,
        dataset_kwargs: dict | None = ...,
        dataset_extra: dict | None = ...,
    ):  # -> None:
        """Add the input dataset and its corresponding hook execution context to the collector."""
        ...

    def add_output_dataset(
        self,
        context: LineageContext,
        scheme: str | None = ...,
        uri: str | None = ...,
        dataset_kwargs: dict | None = ...,
        dataset_extra: dict | None = ...,
    ):  # -> None:
        """Add the output dataset and its corresponding hook execution context to the collector."""
        ...

    @property
    def collected_datasets(self) -> HookLineage:
        """Get the collected hook lineage information."""
        ...

    @property
    def has_collected(self) -> bool:
        """Check if any datasets have been collected."""
        ...

class NoOpCollector(HookLineageCollector):
    """
    NoOpCollector is a hook lineage collector that does nothing.

    It is used when you want to disable lineage collection.
    """

    def add_input_dataset(self, *_, **__):  # -> None:
        ...
    def add_output_dataset(self, *_, **__):  # -> None:
        ...
    @property
    def collected_datasets(self) -> HookLineage: ...

class HookLineageReader(LoggingMixin):
    """Class used to retrieve the hook lineage information collected by HookLineageCollector."""

    def __init__(self, **kwargs) -> None: ...
    def retrieve_hook_lineage(self) -> HookLineage:
        """Retrieve hook lineage from HookLineageCollector."""
        ...

def get_hook_lineage_collector() -> HookLineageCollector:
    """Get singleton lineage collector."""
    ...
