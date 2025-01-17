"""Unit tests for the operators.mlflow module."""

from __future__ import annotations


def test_import():
    from dagcellent.operators.mlflow import GetModelMetaData

    assert GetModelMetaData is not None
