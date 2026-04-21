# Technical Context

## Tech Stack

### Core

- Python 3.10+ in `pyproject.toml`
- `click`
- `requests`
- `jsonschema`
- `semver`
- `json-logic-qubit`
- `pyyaml`
- `jinja2`
- `cookiecutter`
- `python-gitlab`
- `fastapi`
- `uvicorn`

### Styling

- Docusaurus-based docs/dashboard app
- Tailwind CSS in the dashboard app

### State & Data

- JSON schema validation
- JSON Logic rule evaluation
- Schema-driven analyzer and report payloads

### Testing

- `pytest`
- `pytest-cov`
- `responses`
- `httpx`

### Dev Tools

- `ruff`
- `trunk`
- `pipenv`
- `setuptools-scm`

## Development Environment

### Prerequisites

- Python 3.10+
- `pipenv`
- Node toolchain for docs/dashboard work

### Setup Commands

```bash
# Install
pipenv install --dev

# Dev server
pipenv run regis --help
pnpm --filter @regis/dashboard dev

# Build
pnpm run build

# Test
pipenv run pytest
pipenv run pytest --no-cov
```

### Environment Variables

- Not documented in the inspected files

## Project Structure

```text
project-root/
├── regis/
├── apps/
├── docs/
├── scripts/
└── tests/
```

## Import Aliases

- No import alias mapping was found in the inspected files

## Build & Deploy

- GitHub Actions workflows in `.github/workflows/`
- Release Please for releases
- SBOM generation and provenance attestation in CD
- Docusaurus docs deployment
