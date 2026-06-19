"""Base config contracts shared across sources."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class K8sResourceSpec(BaseModel):
    """CPU and memory for K8s (requests or limits)."""

    cpu: str
    memory: str


class K8sResources(BaseModel):
    """K8s requests and limits for a KubernetesPodOperator task."""

    requests: K8sResourceSpec
    limits: K8sResourceSpec


class BaseEntityConfig(BaseModel):
    """Fields the runner reads from every entity config."""

    name: str
    write_disposition: Literal["append", "replace"]
    partition_column: str | None = None
    incremental_column: str | None = None
    schema_contract: dict[str, str] = Field(default_factory=lambda: {"data_type": "freeze"})
    k8s_resources: K8sResources = Field(
        default_factory=lambda: K8sResources(
            requests=K8sResourceSpec(cpu="400m", memory="1Gi"),
            limits=K8sResourceSpec(cpu="800m", memory="2Gi"),
        )
    )


class BaseSourceConfig(BaseModel):
    """Fields the runner reads from every source config."""

    type: str
    domain: str
    source_system: str
    connection_id: str
