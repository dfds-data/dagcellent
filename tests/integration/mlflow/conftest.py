from __future__ import annotations

from pathlib import Path
from warnings import warn

import pytest
import requests
from requests.exceptions import ConnectionError


def _is_responsive(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


def _remove_path(path: Path):
    if path.is_file() or path.is_symlink():
        path.unlink()
        return
    for p in path.iterdir():
        _remove_path(p)
    path.rmdir()


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: pytest.Config):
    return [
        str(pytestconfig.rootpath / "docker-compose.yaml"),
        str(Path(__file__).parent / "docker-compose.override.mlflow.yaml"),
    ]


@pytest.fixture(scope="module", autouse=True)
def mlflow_service(docker_ip, docker_services, pytestconfig: pytest.Config):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("mlflow", 5000)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: _is_responsive(url)
    )
    yield url
    # after run, remove the root 'mlruns' folder
    _p = pytestconfig.rootpath / "mlruns"
    if not _p.exists():
        return

    if _p.is_dir():
        _remove_path(_p)
        return
    warn(
        "Could not clean up `mlruns` artifact. This might cause unexpected"
        "behaviour in the next test suite execution.",
        stacklevel=2,
    )


@pytest.fixture(scope="module")
def mlflow_hook(mlflow_service: str):
    """Get MLFlow client wrapper."""
    from dagcellent.operators.mlflow.hooks import MlflowHook

    return MlflowHook(mlflow_service)
