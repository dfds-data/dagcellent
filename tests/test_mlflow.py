"""Unit tests for the operators.mlflow module."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.mlflow


def test_import():
    from dagcellent.operators.mlflow import GetModelMetaData

    assert GetModelMetaData is not None
