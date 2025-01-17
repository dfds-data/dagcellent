"""This package wraps some functionalities of MLFlows life-cycle management features.

MLflow Skinny: *A Lightweight Machine Learning Lifecycle Platform Client*.


MLflow Skinny is a lightweight MLflow package without SQL storage, server, UI, or data science dependencies. MLflow Skinny supports:
    Tracking operations (logging / loading / searching params, metrics, tags + logging / loading artifacts)
    Model registration, search, artifact loading, and deployment
    Execution of GitHub projects within notebook & against a remote target.
"""

from __future__ import annotations

from dagcellent.operators.mlflow._operators import (
    GetLatestModelVersion,
    GetModelMetaData,
    GetModelVersionByNameAndStage,
    SetModelVersionTag,
)
from dagcellent.operators.mlflow._utils import (
    MlflowModelStage,
    SlimModelVersion,
)

__all__ = [
    "SetModelVersionTag",
    "GetModelVersionByNameAndStage",
    "GetModelMetaData",
    "GetLatestModelVersion",
    "SlimModelVersion",
    "MlflowModelStage",
]
