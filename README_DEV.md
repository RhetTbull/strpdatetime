# Developer Notes

These are notes to myself so I don't forget how to do things but they might be useful for others that want to contribute.

## Setup the environment

- Clone the repository
- Change to the project directory
- Install [uv](https://github.com/astral-sh/uv): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Create the virtual environment: `uv venv` or `uv venv --python 3.13` to specify a specific version
- Activate the virtual environment: `source .venv/bin/activate`
- Install package dependencies: `uv sync --python 3.13 --all-extras` (replace 3.13 with the desired version of Python)

## Testing and Building

- Run mypy: `mypy strpdatetime.py`
- Run tests: `pytest --doctest-glob=README.md  -vv`
- Build the package: `rm -rf dist/ && rm -rf build/ && uv build`

## Bump the version

Edit the version in `pyproject.toml`.

## Changelog

Use [auto-changelog](https://github.com/cookpete/auto-changelog):

- `auto-changelog --ignore-commit-pattern CHANGELOG -l 5`

## Publish to PyPI

- `uv publish`
