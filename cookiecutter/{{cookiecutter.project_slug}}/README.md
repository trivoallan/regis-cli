# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Getting Started

This repository is configured to use `regis-cli` for analyzing container images.

### Running Analysis Locally

You can run the analysis using Docker:

```bash
docker run --rm \
  -v ${PWD}/reports:/app/reports \
  -v ${PWD}/scorecards:/app/scorecards \
  ghcr.io/trivoallan/regis-cli:latest \
  analyze {{ cookiecutter.registry_domain }}/{{ cookiecutter.repository_owner }}/YOUR_IMAGE:TAG \
  -s scorecards/default.yaml \
  -f html
```

### GitHub Actions

A workflow is provided in `.github/workflows/analyze.yml` to automate this analysis.

- **Manual Trigger**: You can manually run the analysis from the "Actions" tab by providing an `image_url`.
- **Automatic Publishing**: Generated reports are committed back to the repository and automatically published to **GitHub Pages**.

To view your reports, enable GitHub Pages in your repository settings and point it to the "GitHub Actions" source.

## Documentation

- [docs/memory-bank/](docs/memory-bank/): Project context and progress tracking.
- [scorecards/](scorecards/): Custom security policies.
