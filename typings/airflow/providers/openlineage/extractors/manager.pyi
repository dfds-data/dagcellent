"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

from airflow.lineage.entities import Table
from airflow.models import Operator
from airflow.providers.openlineage.extractors import BaseExtractor, OperatorLineage
from airflow.utils.log.logging_mixin import LoggingMixin
from openlineage.client.event_v2 import Dataset

if TYPE_CHECKING: ...

class ExtractorManager(LoggingMixin):
    """Class abstracting management of custom extractors."""

    def __init__(self) -> None: ...
    def add_extractor(
        self, operator_class: str, extractor: type[BaseExtractor]
    ):  # -> None:
        ...
    def extract_metadata(
        self, dagrun, task, complete: bool = ..., task_instance=...
    ) -> OperatorLineage: ...
    def get_extractor_class(self, task: Operator) -> type[BaseExtractor] | None: ...
    def extract_inlets_and_outlets(
        self, task_metadata: OperatorLineage, inlets: list, outlets: list
    ):  # -> None:
        ...
    def get_hook_lineage(self) -> tuple[list[Dataset], list[Dataset]] | None: ...
    @staticmethod
    def convert_to_ol_dataset_from_object_storage_uri(uri: str) -> Dataset | None: ...
    @staticmethod
    def convert_to_ol_dataset_from_table(table: Table) -> Dataset: ...
    @staticmethod
    def convert_to_ol_dataset(obj) -> Dataset | None: ...
    def validate_task_metadata(self, task_metadata) -> OperatorLineage | None: ...
