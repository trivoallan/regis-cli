# Decision Log

## 2026-02-20: Handle Skopeo Architecture Mismatch
- **Decision**: Avoid high-level `skopeo inspect` on image indexes when the local architecture doesn't match the remote index.
- **Rationale**: Prevent "no image found" errors (exit status 1) when analyzing multi-arch images on local dev machines (e.g., Apple Silicon).

## 2026-02-20: Automated Docs Publishing
- **Decision**: Implement GitHub Actions workflow to build and publish Antora site to GitLab Pages.
- **Rationale**: Automate documentation deployment to ensure it stays up-to-date with the code.

## 2026-02-20: Cookiecutter Template for Consumer Repos
- **Decision**: Create a Cookiecutter template to bootstrap new repositories for `regis-cli` users.
- **Rationale**: Facilitate adoption and standardize the setup for image analysis projects, including CI/CD and security policies.

## 2026-02-20: Fix Missing Scorecard Values
- **Decision**: Update `evaluate` in `engine.py` to merge `results` into the root context of the `MissingDataTracker`.
- **Decision**: Fix Trivy rule keys in the default scorecard template.
- **Rationale**: Scorecard rules like `trivy.critical_count` were failing because the analyzer data was nested under `results.`. Matching the structure and mapping it to the root simplifies rule writing and fixes `(MISSING)` errors in reports.
