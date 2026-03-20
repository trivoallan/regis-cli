---
sidebar_position: 2
---

# Getting Started

`regis-cli` is a powerful Docker registry analysis tool designed to inspect container images, evaluate security policies via playbooks, and generate comprehensive reports.

## Prerequisites

The requirements depend on whether you use the Docker image or install the tool locally.

- **Core Requirement**:
  \*\* **Skopeo**: Essential for multi-architecture registry inspection and metadata extraction.
- **Optional Analyzers**:
  \*\* **Trivy**: Required for vulnerability scanning and SBOM generation.
  \*\* **Hadolint**: Required for Dockerfile linting.
  \*\* **Dockle**: Required for container image security linting.

## Installation

### Docker (Recommended)

The easiest way to use `regis-cli` without managing local dependencies is to use the official Docker image. It comes pre-packaged with Skopeo, Trivy, Hadolint, and Dockle.

```bash
docker run --rm trivoallan/regis-cli --help
```

### Local Installation

If you prefer a local installation, ensure you have **Python 3.14 or later** and **Skopeo** installed in your system.

```bash
pip install regis-cli
```

:::tip
For developers wanting to contribute to the project, use **Pipenv**:
`pipenv install --dev`
:::

## Run your first analysis

You can analyze any public container image. By default, `regis-cli` produces a JSON report on `stdout`.

```bash
regis-cli analyze nginx:latest
```

### Generating a Web Report

To generate a rich HTML report alongside the JSON report, use the `--site` (or `-s`) flag:

```bash
regis-cli analyze nginx:latest --site
```

Reports are written to the `reports/` directory by default (e.g., `reports/docker.io/library/nginx/sha256-.../index.html`).

## Advanced Tools

`regis-cli` includes specialized subcommands for advanced workflows:

- `bootstrap`: Infrastructure as Code (IaC) for your analysis. Bootstrap a new Git repository or a new playbook.
- `evaluate`: Test playbooks against existing analysis reports without re-fetching image data.
- `gitlab`: Seamless integration with GitLab CI/CD for automated reporting and MR updates.

:::info
Our **[GitLab integration](integrations/gitlab.md)** is currently the most feature-rich, offering automated Merge Request comments, status updates, and deep CI/CD pipeline integration.
:::

## Next steps

- **Custom Playbooks**: Define your own security rules in the [Understand Playbooks](playbooks.md) guide.
- **Project Bootstrapping**: Learn how to use `regis-cli bootstrap` in the [Available Commands](commands.md#bootstrap) guide.
- **CI/CD Integration**: See our guides for [GitHub Workflows](integrations/github.md) and [GitLab CI](integrations/gitlab.md).
