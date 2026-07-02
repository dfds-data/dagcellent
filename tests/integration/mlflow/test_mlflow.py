from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import mlflow
import pytest
import requests

pytestmark = [pytest.mark.integration, pytest.mark.mlflow]
if TYPE_CHECKING:
    from dagcellent.operators.mlflow.hooks import MlflowHook


# def test_status_code_mlflow(mlflow_service: str):
#     status = 200
#     response = requests.get(mlflow_service + "/health")

#     assert response.status_code == status


# def test_get_run(mlflow_hook: MlflowHook):
#     experiment_id = mlflow.create_experiment(
#         "Social NLP Experiments",
#         artifact_location=Path(__file__).parent.joinpath("mlruns").as_uri(),
#         tags={"version": "v1", "priority": "P1"},
#     )
#     experiment = mlflow.get_experiment(experiment_id)
#     assert experiment_id == experiment.experiment_id


# def test_get_latest_model_version(mlflow_hook: MlflowHook):
#     name = "SocialMediaTextAnalyzer"
#     tags = {"nlp.framework": "Spark NLP"}
#     desc = "This sentiment analysis model classifies the tone-happy, sad, angry."

#     client = mlflow.MlflowClient()
#     client.create_registered_model(name, tags, desc)

#     with pytest.raises(ValueError, match=rf".*{name}*"):
#         assert mlflow_hook.get_latest_model_version(name)


# @pytest.mark.skip(reason="Function deprecated in MLFlow 2.9.0")
# def test_transition_model_version_stage(mlflow_hook: MlflowHook):
#     assert True


# @pytest.mark.skip(reason="Module might change substantially.")
# def test_get_latest_versions():
#     assert True


# @pytest.mark.skip(reason="Module might change substantially.")
# def test_set_model_version_tag():
#     assert True


# @pytest.mark.skip(reason="Module might change substantially.")
# def test_search_model_versions_by_name_stage():
#     assert True
