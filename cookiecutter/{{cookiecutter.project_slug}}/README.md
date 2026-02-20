# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Getting Started

This repository is configured to use `regis-cli` for analyzing container images.

### Running Analysis Locally

You can run the analysis using Docker:

```bash
docker run --rm \
  -v ${PWD}/reports:/app/reports \
  -v ${PWD}/playbooks:/app/playbooks \
  {{ cookiecutter.regis_cli_image_url }} \
  analyze {{ cookiecutter.regis_cli_image_url }} \
  -p playbooks/default.yaml \
  --site
```

{% if cookiecutter.platform == "github" -%}
### GitHub Actions

A workflow is provided in `.github/workflows/analyze.yml` to automate this analysis.

- **Manual Trigger**: You can manually run the analysis from the "Actions" tab by providing an `image_url`.
- **Metadata Traceability**: Reports automatically include GitHub Actions metadata (requester, workflow, run ID) for better auditability.
- **Automatic Publishing**: Generated reports are committed back to the repository and automatically published to **GitHub Pages**.

To view your reports, enable GitHub Pages in your repository settings and point it to the "GitHub Actions" source.
{%- elif cookiecutter.platform == "gitlab" -%}
### GitLab CI

A workflow is provided in `.gitlab-ci.yml` to automate this analysis.

- **Manual Trigger**: You can manually run the analysis from the "Build > Pipelines" tab by providing an `image_url`.
- **Metadata Traceability**: Reports automatically include GitLab CI metadata (requester, job ID, pipeline URL) for better auditability.
- **Automatic Publishing**: Generated reports are committed back to the repository and automatically published to **GitLab Pages**.

To view your reports, ensure GitLab Pages is enabled for your project.
{%- endif %}

## Documentation

- [docs/memory-bank/](docs/memory-bank/): Project context and progress tracking.
- [playbooks/](playbooks/): Custom security policies.
