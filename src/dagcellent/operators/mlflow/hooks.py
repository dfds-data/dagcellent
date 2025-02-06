"""Wrapper around MLflowClient-python package."""
# ruff: noqa: G004

from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING, TypeVar
from warnings import warn

import mlflow
from airflow.hooks.base import BaseHook
from typing_extensions import ParamSpec

if TYPE_CHECKING:
    # NOTE ruff fails for this check
    from collections.abc import Callable

    import mlflow.entities.model_registry  # noqa: TCH004

    from dagcellent.operators.mlflow._utils import MlflowModelStage


_LOGGER = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


def _mlflow_request_wrapper(query: Callable[P, T]) -> T:
    """Wrap requests around MlflowException."""
    try:
        res = query()
    except mlflow.MlflowException as exc:
        _msg = "Error during mlflow query."
        _LOGGER.error(_msg, exc_info=exc)
        raise mlflow.MlflowException(_msg) from exc
    return res


# Public API
class MlflowHook(BaseHook):
    """MLFlow python API hook."""

    conn_name_attr = "mlflow_conn_id"
    default_conn_name = "mlflow_default"
    conn_type = "mlflow"
    hook_name = "Mlflow"

    def __init__(self: MlflowHook, tracking_uri: str) -> None:
        """Create Mlflow python client connection."""
        super().__init__()
        # connection secrets
        self.client = mlflow.MlflowClient(tracking_uri=tracking_uri)

    def get_latest_model_version(
        self: MlflowHook, model_name: str
    ) -> mlflow.entities.model_registry.ModelVersion:
        """Given a model name, return the latest/highest model version.

        Args:
            model_name (str): MLFlow model name

        Returns:
            dict: hashmap with version and run_id of latest model
        """
        query = functools.partial(
            self.client.search_model_versions, f"name = '{model_name}'"
        )
        model_reigstry_info = _mlflow_request_wrapper(query)
        latest_version = functools.reduce(
            lambda x, y: x if int(x.version) > int(y.version) else y,
            model_reigstry_info,
        )
        logging.info(f"{latest_version=}")
        return latest_version

    def get_run(self: MlflowHook, run_id: str) -> mlflow.entities.Run:
        """Return run meta data.

        Wrapper around get_run.

        Args:
            run_id (str): unique run id

        Returns:
            (MlFlow.Run) run meta data
        """
        query = functools.partial(self.client.get_run, run_id)
        return _mlflow_request_wrapper(query)

    def transition_model_version_stage(
        self: MlflowHook,
        name: str,
        version: str,
        stage: str,
        *,
        archive_existing_versions: bool,
    ) -> mlflow.entities.model_registry.ModelVersion:
        """Transition model stage.

        Wrapper around transition_model_version

        Args:
            name (str): name of MLFlow model
            version (str): version of model to transition
            stage (str): target stage to transition to
            archive_existing_versions (bool): to archive current model in 'stage'

        Returns:
            mlflow.entities.model_registry.ModelVersion: model version
        """
        query = functools.partial(
            self.client.transition_model_version_stage,
            name,
            version,
            stage,
            archive_existing_versions,
        )
        return _mlflow_request_wrapper(query)

    def get_latest_versions(
        self: MlflowHook,
        name: str,
        stages: list[str],
    ) -> list[mlflow.entities.model_registry.ModelVersion]:
        """Get latest model version. See MLFlow docs.

        Wrapper around get_latest_versions.

        Args:
            name (str): model name
            stages (list[str]): stages

        Returns:
            list[mlflow.entities.model_registry.ModelVersion]: list of model versions
        """
        warn("This is deprecated in mlflow 2.9.0", DeprecationWarning, stacklevel=2)
        query = functools.partial(self.client.get_latest_versions, name, stages)
        return _mlflow_request_wrapper(query)

    def set_model_version_tag(
        self: MlflowHook, model_name: str, version: str, tag: dict[str, str]
    ) -> None:
        """Set a tag for the model version. When stage is set, tag will be set for latest model version of the stage.

        Setting both version and stage parameter will result in error.

        """
        logging.debug(f"{model_name!r} {version!r} {tag!r}")
        for k, v in tag.items():
            self.client.set_model_version_tag(model_name, version, k, v)

    def search_model_versions_by_name_stage(
        self: MlflowHook,
        name: str,
        stage: MlflowModelStage,
    ) -> list[mlflow.entities.model_registry.ModelVersion]:
        """Get model by name and stage tag. See MLFlow docs.

        Wrapper around search_model_versions.

        Args:
            name (str): model name
            stage (MlflowModelStage): stage

        Returns:
            list[mlflow.entities.model_registry.ModelVersion]: list of model versions
        """
        logging.debug(f"{name!r} {stage!r}")
        _stage = stage.value
        _filter = f"name='{name}' AND tag.stage='{_stage}'"
        query = functools.partial(self.client.search_model_versions, _filter)
        return _mlflow_request_wrapper(query)
