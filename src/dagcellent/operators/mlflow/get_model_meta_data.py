from __future__ import annotations

import logging
from typing import Any

from airflow.models.baseoperator import BaseOperator

from dagcellent.operators.mlflow.hooks import MlflowHook


class GetModelMetaData(BaseOperator):
    """Wrapper around MLFlowClient.get_run."""

    ui_color = "#78cbf7"

    def __init__(
        self,
        tracking_uri: str,
        upstream_task_id: str,
        **kwargs,
    ) -> None:
        """Get model metadata, where run_id provided as upstream task's id.

        Args:
            tracking_uri (str):  Mlflow.client tracking URI
            upstream_task_id (str): xcom which has `run_id` key.
            kwargs: BaseOperator args
        """
        self.tracking_uri = tracking_uri
        self.upstream_task_id = upstream_task_id

        super().__init__(**kwargs)

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
            _first_item = xcom_val.pop()
            run_id = _first_item["run_id"]
            logging.warning(
                "Multiple items returned from upstream task. Defaulting to first item"
            )
        elif isinstance(xcom_val, dict):
            run_id = xcom_val["run_id"]
        else:
            logging.error(
                f"Operator has no implementation for this type: {type(xcom_val)}."
            )
            raise NotImplementedError
        logging.info(f"{run_id=}")
        data = client_hook.get_run(run_id)
        logging.info(f"{data=}")
        return data.data.metrics
