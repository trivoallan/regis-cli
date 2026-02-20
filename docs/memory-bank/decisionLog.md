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
- **Decision**: Fixed Docker permission issues by creating a home directory for the `regis` user (UID 1001), adjusting volume permissions in the workflow, and adding a fallback output mechanism in `cli.py`.
- **Decision**: Created comprehensive Cookiecutter usage guide in `docs/modules/ROOT/pages/cookiecutter.adoc`.
- **Decision**: Update template workflow to `chmod 777 reports` before analysis.
- **Rationale**: Address "permission denied" errors on both `/home/regis` (due to missing home/UID mismatch) and on host-mounted `reports` volumes. UID 1001 matches standard GitHub Actions runners.
