# regis-cli

CLI tool to analyze Docker image registries and produce JSON reports.

## Features

- **Pluggable analyzers** — each analyzer is a Python module producing a JSON report validated by a dedicated JSON Schema
- **Entry-points architecture** — add new analyzers without modifying core code
- **Docker Registry V2 API** — supports Docker Hub and any V2-compatible registry

### Built-in Analyzers

| Analyzer | Description |
|----------|-------------|
| `tags`   | Lists all available tags for a repository |
| `image`  | Inspects image metadata (architecture, OS, labels, layers) |

## Installation

```bash
pipenv install
```

## Usage

```bash
# Analyze an image (all analyzers)
regis-cli analyze https://hub.docker.com/r/library/nginx --pretty

# Run a specific analyzer
regis-cli analyze nginx:latest --analyzer tags

# List available analyzers
regis-cli list

# Write output to file
regis-cli analyze nginx --output report.json
```

## Development

```bash
# Install with dev dependencies
pipenv install --dev

# Run tests
pipenv run pytest -v

# Run with verbose logging
regis-cli -v analyze nginx:latest
```

## Adding a New Analyzer

1. Create a module in `regis_cli/analyzers/` inheriting from `BaseAnalyzer`
2. Create a JSON Schema in `regis_cli/schemas/`
3. Register the entry point in `pyproject.toml`:

```toml
[project.entry-points."regis_cli.analyzers"]
myanalyzer = "regis_cli.analyzers.myanalyzer:MyAnalyzer"
```

4. Reinstall: `pipenv install`

## Documentation

See the [docs/](docs/) directory for detailed documentation (Antora).

## License

MIT
