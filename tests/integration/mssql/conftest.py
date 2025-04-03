from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from warnings import warn

import pymssql
import pytest
from sqlalchemy import create_engine

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

SERVICE_PORT = 1433
TEST_CONNECTION_URL = f"mssql+pymssql://sa:Alma1234@localhost:{SERVICE_PORT}"


def _is_responsive(url: str):
    try:
        # if `connect()` is successful, the service is up
        _ = create_engine(url).connect()
    except pymssql.exceptions.OperationalError:
        return False
    return True


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: pytest.Config):
    return [
        str(pytestconfig.rootpath / "docker-compose.yaml"),
        str(Path(__file__).parent / "docker-compose.override.mssql.yaml"),
    ]


@pytest.fixture(scope="module", autouse=True)
def mssql_service(docker_ip, docker_services, pytestconfig: pytest.Config):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    _ = docker_services.port_for("db", SERVICE_PORT)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: _is_responsive(TEST_CONNECTION_URL)
    )


@pytest.fixture(scope="module")
def db_engine(mssql_service: None) -> Engine:
    """Get a mssql sqlalchemy.engine.Engine object.

    The service is reachable and a "dbo.test" table is populated with dummy
    data. See `./tests/integration/mssql/mssql_init.sql`
    """
    yield create_engine(TEST_CONNECTION_URL)
    warn("Cleanup", stacklevel=2)
