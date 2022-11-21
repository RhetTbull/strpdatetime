# Developer Notes

These are notes to myself so I don't forget how to do things but they might be useful for others that want to contribute.

## Setup

- Clone the repository
- Install poetry: `pip install poetry`
- Install dependencies: `poetry install`
- Run mypy: `poetry run mypy strpdatetime.py`
- Run tests: `poetry run pytest --doctest-glob=README.md  -vv`
- Build the package: `rm -rf dist/ && rm -rf build/ && poetry build`
