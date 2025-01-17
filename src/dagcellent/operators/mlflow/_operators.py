from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from airflow.models.baseoperator import BaseOperator

from dagcellent.operators.mlflow._utils import (
    MlflowModelStage,
    SlimModelVersion,
    serialize_model_version,
)
from dagcellent.operators.mlflow.hooks import MlflowHook

if TYPE_CHECKING:
    from collections.abc import Sequence


class SetModelVersionTag(BaseOperator):
    """Wrapper around MLFlowClient.set_model_version_tag.

    Tags have to be passed in as key-value pairs. Multiple tags can be set.
    """

    template_fields: Sequence[str] = (
        "model_name",
        "version",
        "tag",
    )
    ui_color = "#78cbf7"

    def __init__(
        self,
        tracking_uri: str,
        model_name: str,
        version: str,
        tag: dict[str, str],
        **kwargs: Any,
    ) -> None:
        """Get model metadata, where run_id provided as upstream task's id.

        Args:
            tracking_uri (str):  Mlflow.client tracking URI
            model_name (str): mlfow model name e.g.: `batch`
            version: (str): model version
            tag: arbitrary tag in `{key: value}` format
            kwargs: BaseOperator args
        """
        self.tracking_uri = tracking_uri
        self.model_name = model_name
        self.version = version
        self.tag = tag

        super().__init__(**kwargs)  # type: ignore [reportUnknownMemberType]

    def execute(self, context: Any) -> None:
        """Operator execute method.

        Args:
            context (Any): Airflow context

        Returns:
            _type_: metrics data
        """
        client_hook = MlflowHook(self.tracking_uri)
        return client_hook.set_model_version_tag(
            self.model_name, self.version, self.tag
        )


class GetModelVersionByNameAndStage(BaseOperator):
    """Wrapper around MLflow search_model_versions limited by name and tag.stage.

    Example:
        ```python
        # Get prod model run id
        from dagcellent.operators.mlflow import (
            GetModelVersionByNameAndStage,
            MlflowModelStage,
        )

        get_prod_run_id = GetModelVersionByNameAndStage(
            task_id="get_prod_run_id",
            tracking_uri="<login>:<password>@<domain>/<login>/mlflow",
            model_name="<skynet-auto>",
            stage=MlflowModelStage.PRODUCTION,
        )
        ```
    """

    ui_color = "#78cbf7"

    def __init__(
        self,
        tracking_uri: str,
        model_name: str,
        stage: MlflowModelStage,
        **kwargs: Any,
    ) -> None:
        """Latest model version for stage.

        If no ``stage`` provided, returns the latest version for each stage.

        Args:
            tracking_uri (str): Mlflow.client tracking URI
            model_name (str): MLFlow model name
            stage (MlflowModelStage): target stage to transition to
            kwargs: BaseOperator args
        """
        self.tracking_uri = tracking_uri
        self.stage = stage
        self.model_name = model_name

        super().__init__(**kwargs)  # type: ignore [reportUnknownMemberType]

    def execute(self, context: Any) -> list[SlimModelVersion]:
        """Connect to Mlflow hook and dump messages to tmp file."""
        client_hook = MlflowHook(self.tracking_uri)
        model_versions = client_hook.search_model_versions_by_name_stage(
            name=self.model_name, stage=self.stage
        )
        # This could be more general, but then it would be more complicated to get run_id form xcom
        # in later steps.
        _models_infos = [serialize_model_version(x) for x in model_versions]
        return _models_infos


class GetModelMetaData(BaseOperator):
    """Wrapper around MLFlowClient.get_run."""

    ui_color = "#78cbf7"

    def __init__(
        self,
        tracking_uri: str,
        upstream_task_id: str,
        **kwargs: Any,
    ) -> None:
        """Get model metadata, where run_id provided as upstream task's id.

        Args:
            tracking_uri (str):  Mlflow.client tracking URI
            upstream_task_id (str): xcom which has `run_id` key.
            kwargs: BaseOperator args
        """
        self.tracking_uri = tracking_uri
        self.upstream_task_id = upstream_task_id

        super().__init__(**kwargs)  # type: ignore [reportUnknownMemberType]

    def execute(self, context: Any) -> Any:
        """Operator execute method.

        Args:
            context (Any): Airflow context

        Returns:
            _type_: metrics data
        """
        client_hook = MlflowHook(self.tracking_uri)
        xcom_val = context["task_instance"].xcom_pull(
            key="return_value", task_ids=self.upstream_task_id
        )
        if isinstance(xcom_val, list):
            _first_item = xcom_val.pop()  # type: ignore [unknownTypeIssue]
            run_id = _first_item["run_id"]  # type: ignore [unknownTypeIssue]
            logging.warning(
                "Multiple items returned from upstream task. Defaulting to first item"
            )
        elif isinstance(xcom_val, dict):
            run_id = xcom_val["run_id"]  # type: ignore [unknownTypeIssue]
        else:
            logging.error(
                "Operator has no implementation for this type: %s", f"{type(xcom_val)}."
            )
            raise NotImplementedError
        logging.info("%s", f"{run_id=}")
        if not isinstance(run_id, str):
            raise ValueError(f"{run_id} must be an instance of 'str'")
        data = client_hook.get_run(run_id)
        logging.info("%s", f"{data=}")
        return data.data.metrics  # type: ignore [unknownTypeIssue]


class GetLatestModelVersion(BaseOperator):
    """Custom wrapper around MLFlowClient.search_model_versions."""

    ui_color = "#78cbf7"

    def __init__(
        self,
        tracking_uri: str,
        model_name: str,
        **kwargs: Any,
    ) -> None:
        """Find highest version number of model.

        Args:
            tracking_uri (str): MLFlow tracking server uri
            model_name (str): name of MLFlow Model
            kwargs (Any): BaseOperator kwargs

        Returns:
            (dict) {"version": latest_version.version, "run_id": latest_version.run_id}
        """
        self.tracking_uri = tracking_uri
        self.model_name = model_name

        super().__init__(**kwargs)  # type: ignore [reportUnknownMemberType]

    def execute(self, context: Any) -> SlimModelVersion:
        """Operator execute method.

        Args:
            context (Any): Airflow context

        Returns:
            dict
        """
        client_hook = MlflowHook(self.tracking_uri)
        return serialize_model_version(
            client_hook.get_latest_model_version(self.model_name)
        )
