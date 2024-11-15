from __future__ import annotations

from typing import TYPE_CHECKING, Any

from airflow.models.baseoperator import BaseOperator

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
        **kwargs,
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

        super().__init__(**kwargs)

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
