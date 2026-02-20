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
- **Decision**: Integrate GitHub Actions metadata into the template workflow using `regis-cli -m`.
- **Rationale**: Providing workflow context (requester, run ID) directly in the report improves auditability and helps users identify the origin of an automated report.
