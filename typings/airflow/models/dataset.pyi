"""
This type stub file was generated by pyright.
"""

from airflow.datasets import Dataset, DatasetAlias
from airflow.models.base import Base

alias_association_table = ...
dataset_alias_dataset_event_association_table = ...

class DatasetAliasModel(Base):
    """
    A table to store dataset alias.

    :param uri: a string that uniquely identifies the dataset alias
    """

    id = ...
    name = ...
    __tablename__ = ...
    __table_args__ = ...
    datasets = ...
    dataset_events = ...
    consuming_dags = ...
    @classmethod
    def from_public(cls, obj: DatasetAlias) -> DatasetAliasModel: ...
    def __repr__(self):  # -> str:
        ...
    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...

class DatasetModel(Base):
    """
    A table to store datasets.

    :param uri: a string that uniquely identifies the dataset
    :param extra: JSON field for arbitrary extra info
    """

    id = ...
    uri = ...
    extra = ...
    created_at = ...
    updated_at = ...
    is_orphaned = ...
    consuming_dags = ...
    producing_tasks = ...
    __tablename__ = ...
    __table_args__ = ...
    @classmethod
    def from_public(cls, obj: Dataset) -> DatasetModel: ...
    def __init__(self, uri: str, **kwargs) -> None: ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self):  # -> str:
        ...

class DagScheduleDatasetAliasReference(Base):
    """References from a DAG to a dataset alias of which it is a consumer."""

    alias_id = ...
    dag_id = ...
    created_at = ...
    updated_at = ...
    dataset_alias = ...
    dag = ...
    __tablename__ = ...
    __table_args__ = ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self):  # -> str:
        ...

class DagScheduleDatasetReference(Base):
    """References from a DAG to a dataset of which it is a consumer."""

    dataset_id = ...
    dag_id = ...
    created_at = ...
    updated_at = ...
    dataset = ...
    dag = ...
    queue_records = ...
    __tablename__ = ...
    __table_args__ = ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self):  # -> str:
        ...

class TaskOutletDatasetReference(Base):
    """References from a task to a dataset that it updates / produces."""

    dataset_id = ...
    dag_id = ...
    task_id = ...
    created_at = ...
    updated_at = ...
    dataset = ...
    __tablename__ = ...
    __table_args__ = ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self):  # -> str:
        ...

class DatasetDagRunQueue(Base):
    """Model for storing dataset events that need processing."""

    dataset_id = ...
    target_dag_id = ...
    created_at = ...
    dataset = ...
    __tablename__ = ...
    __table_args__ = ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self):  # -> str:
        ...

association_table = ...

class DatasetEvent(Base):
    """
    A table to store datasets events.

    :param dataset_id: reference to DatasetModel record
    :param extra: JSON field for arbitrary extra info
    :param source_task_id: the task_id of the TI which updated the dataset
    :param source_dag_id: the dag_id of the TI which updated the dataset
    :param source_run_id: the run_id of the TI which updated the dataset
    :param source_map_index: the map_index of the TI which updated the dataset
    :param timestamp: the time the event was logged

    We use relationships instead of foreign keys so that dataset events are not deleted even
    if the foreign key object is.
    """

    id = ...
    dataset_id = ...
    extra = ...
    source_task_id = ...
    source_dag_id = ...
    source_run_id = ...
    source_map_index = ...
    timestamp = ...
    __tablename__ = ...
    __table_args__ = ...
    created_dagruns = ...
    source_aliases = ...
    source_task_instance = ...
    source_dag_run = ...
    dataset = ...
    @property
    def uri(self): ...
    def __repr__(self) -> str: ...
