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

## 2026-02-20: Fix Docker Permission Issues
- **Decision**: Update `Dockerfile` to create a home directory for the `regis` user and set `HOME`.
- **Decision**: Update template workflow to `chmod 777 reports` before analysis.
- **Rationale**: Fix "permission denied" errors when running analyzers like Trivy (which need a home dir for cache) and when writing reports to host-mounted volumes in CI/CD.
