---
trigger: always_on
---

# Commit messages

- Must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. Allowed types : https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#type
- Scopes are **mandatory** and must be extrapolated from the architectural component modified.
- Styleguide : https://developers.google.com/blockly/guides/contribute/get-started/commits

## Defined Scopes

To ensure clean and readable changelogs, please use the following allowed scopes depending on the architectural component modified:

### Core & Logic
- `cli` : Changes to the command-line interface, argument parsing, or main console output.
- `playbook` : The rule evaluation engine, section parsing, `jsonLogic` resolution, and context management.
- `schema` : Data interfaces, structure definition, and JSON validation files (`*.schema.json`).
- `registry` : The registry communication layer (HTTP requests, authentication, manifest fetching).

### Analyzers
- `analyzer` : Changes to the base analyzer class or shared analyzer interfaces.
- `analyzer/trivy` : Specific to vulnerability scanning and SBOM generation via Trivy.
- `analyzer/sbom` : Specific to SBOM analysis and CycloneDX/SPDX generation.
- `analyzer/hadolint` : Specific to Dockerfile linting.
- `analyzer/skopeo` : Specific to base metadata extraction.

- `analyzer/freshness` : Specific to image age and freshness score calculations.
- `analyzer/size` : Specific to size and layer calculations.
- `analyzer/popularity` : Specific to registry popularity metrics.
- `analyzer/endoflife` : Specific to version support status.
- `analyzer/scorecarddev` : Specific to OpenSSF Scorecard checks.
- `analyzer/provenance` : Specific to provenance and supply chain evidence.

### Rendering & Reporting
- `report` : High-level report generation logic (folder creation, file writing).
- `templates` (or `theme`) : Visual aspects, HTML structure, CSS stylesheets, and Jinja2 macros.

### Tooling & CI
- `ci` : GitHub Actions workflows (Super-Linter, release-please, etc.).
- `deps` (or `build`) : Environment management (Pipenv, pyproject.toml, Dockerfiles).
- `docs` : Antora documentation, READMEs, and Memory Bank updates.