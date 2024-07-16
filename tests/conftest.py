from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def toml_file(tmp_path_factory: pytest.TempPathFactory):
    TOML_TEST = """version = 1
    description = "test"
    """
    fn = tmp_path_factory.mktemp("test") / "test.toml"
    with open(fn, "w+") as f:
        f.writelines(TOML_TEST)

    return fn
