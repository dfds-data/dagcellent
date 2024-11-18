Thank you for contributing to Dagcellent or even considering it.

# Build system
[🐣 Hatch](https://hatch.pypa.io/latest/)

Also see [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml)

Install hatch with `pipx` and configure it. As a minimum, configure it to create `venv` in your project folder:
```toml
[dirs.env]
virtual = ".venv"
```

# VSCode
1. Clone the repo
1. Run `hatch env create && hatch env create dev && hatch env create test`
1. Open VSCode `code .`
1. Select the `dev` environment for development [See the documentation.](https://hatch.pypa.io/latest/how-to/integrate/vscode/)

To enable test discovery and test debugging, change the *python interpreter path* to a test environments path e.g. `test.py3.11`.

# No VSCode
I suggest NeoVim or Zed. See the cheat-sheet below.

# Cheat sheet
- tests: `hatch test`
- docs: `hatch run dev:docs`

# Documentation
The docs is built into "sites" folder. This is gitignored and the docs is built in CI.

The latest version of the documentation is available on a github pages site, linked in the github repo.

To preview the documentation locally, you need to start mkdocs server. See [Go to Cheat sheet](#cheat-sheet)  

## Stable/User documentation

The deployment manifests and Dockerfile for the k8s hosted docs site is under `k8s/`


# Releases
We release the package to a private package feed in ADO under "The Compass" project "compass" feed.

The project uses semantic versioning.

## Changelog Generation
## Update CHANGELOG and CONTRIBUTORS
`git-cliff` is used for changelog generation.

We do not separate between `developer` and `user` changelog/news. The changelog is directly pulled from your git commits. Hence, it is necessary to write commits according to conventional commits.

## Versioning
The package follows semantic versioning. Breaking changes will occur unannounced before `v1.0.0`. After that all breaking changes will lead to bumping the major version number.


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
