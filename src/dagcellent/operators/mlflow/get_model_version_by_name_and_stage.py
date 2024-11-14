from __future__ import annotations

from typing import Any

from airflow.models.baseoperator import BaseOperator

from dagcellent.operators.mlflow.hooks import MlflowHook, MlflowModelStage


class GetModelVersionByNameAndStage(BaseOperator):
    """Wrapper around MLflow search_model_versions limited by name and tag.stage."""

    ui_color = "#78cbf7"

    def __init__(
        self,
        tracking_uri: str,
        model_name: str,
        stage: MlflowModelStage,
        **kwargs,
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

        super().__init__(**kwargs)

    def execute(self, context: Any) -> list[SlimModelVersion]:
        """Connect to Mlflow hook and dump messages to tmp file."""
        client_hook = MlflowHook(self.tracking_uri)
        model_versions = client_hook.search_model_versions_by_name_stage(
            name=self.model_name, stage=self.stage
        )
        # This could be more general, but then it would be more complicated to get run_id form xcom
        # in later steps.
        _models_infos = [_serialize_model_version(x) for x in model_versions]
        return _models_infos
