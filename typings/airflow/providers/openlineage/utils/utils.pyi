"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, Any

from airflow.models import DAG, BaseOperator, DagRun, MappedOperator, TaskInstance
from airflow.providers.common.compat.assets import Asset
from airflow.providers.openlineage.plugins.facets import (
    AirflowDebugRunFacet,
    AirflowJobFacet,
    AirflowRunFacet,
    AirflowStateRunFacet,
)
from airflow.utils.log.secrets_masker import SecretsMasker
from airflow.utils.session import provide_session
from airflow.utils.state import DagRunState, TaskInstanceState
from openlineage.client.event_v2 import Dataset as OpenLineageDataset
from openlineage.client.facet_v2 import RunFacet, processing_engine_run

if TYPE_CHECKING: ...
else: ...
log = ...
_NOMINAL_TIME_FORMAT = ...

def try_import_from_string(string: str) -> Any: ...
def get_operator_class(task: BaseOperator) -> type: ...
def get_job_name(task: TaskInstance) -> str: ...
def get_airflow_mapped_task_facet(task_instance: TaskInstance) -> dict[str, Any]: ...
def get_user_provided_run_facets(
    ti: TaskInstance, ti_state: TaskInstanceState
) -> dict[str, RunFacet]: ...
def get_fully_qualified_class_name(operator: BaseOperator | MappedOperator) -> str: ...
def is_operator_disabled(operator: BaseOperator | MappedOperator) -> bool: ...
def is_selective_lineage_enabled(obj: DAG | BaseOperator | MappedOperator) -> bool:
    """If selective enable is active check if DAG or Task is enabled to emit events."""
    ...

@provide_session
def is_ti_rescheduled_already(ti: TaskInstance, session=...):  # -> bool:
    ...

class InfoJsonEncodable(dict):
    """
    Airflow objects might not be json-encodable overall.

    The class provides additional attributes to control
    what and how is encoded:

    * renames: a dictionary of attribute name changes
    * | casts: a dictionary consisting of attribute names
      | and corresponding methods that should change
      | object value
    * includes: list of attributes to be included in encoding
    * excludes: list of attributes to be excluded from encoding

    Don't use both includes and excludes.
    """

    renames: dict[str, str] = ...
    casts: dict[str, Any] = ...
    includes: list[str] = ...
    excludes: list[str] = ...
    def __init__(self, obj) -> None: ...

class DagInfo(InfoJsonEncodable):
    """Defines encoding DAG object to JSON."""

    includes = ...
    casts = ...
    renames = ...
    @classmethod
    def serialize_timetable(cls, dag: DAG) -> dict[str, Any]: ...

class DagRunInfo(InfoJsonEncodable):
    """Defines encoding DagRun object to JSON."""

    includes = ...

class TaskInstanceInfo(InfoJsonEncodable):
    """Defines encoding TaskInstance object to JSON."""

    includes = ...
    casts = ...

class AssetInfo(InfoJsonEncodable):
    """Defines encoding Airflow Asset object to JSON."""

    includes = ...

class TaskInfo(InfoJsonEncodable):
    """Defines encoding BaseOperator/AbstractOperator object to JSON."""

    renames = ...
    includes = ...
    casts = ...

class TaskInfoComplete(TaskInfo):
    """Defines encoding BaseOperator/AbstractOperator object to JSON used when user enables full task info."""

    includes = ...
    excludes = ...

class TaskGroupInfo(InfoJsonEncodable):
    """Defines encoding TaskGroup object to JSON."""

    renames = ...
    includes = ...

def get_airflow_dag_run_facet(dag_run: DagRun) -> dict[str, RunFacet]: ...
def get_processing_engine_facet() -> dict[
    str, processing_engine_run.ProcessingEngineRunFacet
]: ...
def get_airflow_debug_facet() -> dict[str, AirflowDebugRunFacet]: ...
def get_airflow_run_facet(
    dag_run: DagRun,
    dag: DAG,
    task_instance: TaskInstance,
    task: BaseOperator,
    task_uuid: str,
) -> dict[str, AirflowRunFacet]: ...
def get_airflow_job_facet(dag_run: DagRun) -> dict[str, AirflowJobFacet]: ...
def get_airflow_state_run_facet(
    dag_id: str, run_id: str, task_ids: list[str], dag_run_state: DagRunState
) -> dict[str, AirflowStateRunFacet]: ...
def get_unknown_source_attribute_run_facet(
    task: BaseOperator, name: str | None = ...
):  # -> dict[str, dict[str, Any]]:
    ...

class OpenLineageRedactor(SecretsMasker):
    """
    This class redacts sensitive data similar to SecretsMasker in Airflow logs.

    The difference is that our default max recursion depth is way higher - due to
    the structure of OL events we need more depth.
    Additionally, we allow data structures to specify data that needs not to be
    redacted by specifying _skip_redact list by deriving RedactMixin.
    """

    @classmethod
    def from_masker(cls, other: SecretsMasker) -> OpenLineageRedactor: ...

def is_json_serializable(item):  # -> bool:
    ...
def print_warning(
    log,
):  # -> Callable[..., _Wrapped[Callable[..., Any], Any, Callable[..., Any], Any | None]]:
    ...
def get_filtered_unknown_operator_keys(operator: BaseOperator) -> dict: ...
def should_use_external_connection(hook) -> bool: ...
def translate_airflow_asset(asset: Asset, lineage_context) -> OpenLineageDataset | None:
    """
    Convert an Asset with an AIP-60 compliant URI to an OpenLineageDataset.

    This function returns None if no URI normalizer is defined, no asset converter is found or
    some core Airflow changes are missing and ImportError is raised.
    """
    ...
