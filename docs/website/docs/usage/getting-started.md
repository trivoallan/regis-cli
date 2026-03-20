---
sidebar_position: 1
---

# Getting Started

`regis-cli` is designed to be easy to set up and run, whether locally or in a CI/CD environment.

## Prerequisites

- **Python 3.10+**: Ensure you have Python installed.
- **Docker**: For running certain analyzers like Trivy or Hadolint locally.
- **Pipenv**: (Recommended) For managing dependencies.

## Installation

You can install `regis-cli` via `pip`:

```bash
pip install regis-cli
```

Or using `pipenv`:

```bash
pipenv install regis-cli
```

## Your First Analysis

Once installed, you can analyze any public container image with a single command:

```bash
regis analyze alpine:latest
```

This will:

1. Fetch metadata via **Skopeo**.
2. Run security scans via **Trivy**.
3. Evaluate the default playbook.
4. Generate an HTML report in the `output/` directory.

## What's Next?

- Learn how to create a [Custom Playbook](./custom-playbook.md).
- Understand how [Analyzers](../concepts/analyzers.md) work.
- Integrate `regis-cli` into your [CI/CD Pipeline](./integrations/github.md).
