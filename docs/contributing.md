Thank you for contributing to Dagcellent.

# Build system
[🐣 Hatch](https://hatch.pypa.io/latest/)

# Releases
We release the package to a private package feed in ADO under "The Compass" project "compass" feed.

# Versioning
The package follows semantic versioning. Breaking changes will occur unannounced before `v1.0.0`. After that all breaking changes will lead to bumping the major version number.

# VSCode
1. Clone the repo
1. Run `hatch env create && hatch env create dev && hatch env create test`
1. Open VSCode `code .`
1. Select the `dev` environment for development [See the documentation.](https://hatch.pypa.io/latest/how-to/integrate/vscode/)

To enable test discovery and test debugging, change the *python interpreter path* to a test environments path e.g. `test.py3.11`.

# No VSCode
Cheat sheet:
- tests: `hatch test`

# Docker
The base Dockerfile can be used to run Airflow and install dagcellent in _editable_ mode, so it gives you a short feedback loop.

# tests
## Unit tests
### Fuzzing/hypothesis

## Integration tests
The CI will run integration tests, where external components are not mocked, but real containerized entities are used.


The following integrations are available (docker commands should be executed from the project root folder):
- mssql: `docker compose -f docker-compose.yaml -f ./tests/integration/docker-compose.override.mssql.yaml up --detach`
- psql: `docker compose -f docker-compose.yaml -f ./tests/integration/docker-compose.override.psql.yaml up --detach`

To stop the running instances, it is a good idea to use the `volumes` flag to remove persistent data:
`docker compose -f docker-compose.yaml -f ./tests/integration/docker-compose.override.mssql.yaml down`
