from __future__ import annotations

from typing import Any

from airflow.models.baseoperator import BaseOperator

from dagcellent.operators.mlflow.hooks import MlflowHook


class GetLatestModelVersion(BaseOperator):
    """Custom wrapper around MLFlowClient.search_model_versions."""

    ui_color = "#78cbf7"

    def __init__(
        self,
        tracking_uri: str,
        model_name: str,
        **kwargs,
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

        super().__init__(**kwargs)

    def execute(self, context: Any) -> SlimModelVersion:
        """Operator execute method.

        Args:
            context (Any): Airflow context

        Returns:
            dict
        """
        client_hook = MlflowHook(self.tracking_uri)
        return _serialize_model_version(
            client_hook.get_latest_model_version(self.model_name)
        )
