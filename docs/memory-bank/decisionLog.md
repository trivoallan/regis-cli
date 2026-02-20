# Decision Log

## 2026-02-20: Transition to Least-Privilege Workflow Permissions
- **Decision**: Remove write permissions from top-level workflow blocks.
- **Rationale**: Adhering to GitHub security best practices by only granting write access at the specific job level where it's actually needed.

## 2026-02-20: Documentation as Code with Antora
- **Decision**: Use Antora for documentation and maintain a Memory Bank in `docs/memory-bank/`.
- **Rationale**: Aligning with project rules for structured, maintainable, and versioned documentation.

## 2026-02-20: Handle Skopeo Architecture Mismatch
- **Decision**: Avoid high-level `skopeo inspect` on image indexes when the local architecture doesn't match the remote index.
- **Rationale**: Prevent "no image found" errors (exit status 1) when analyzing multi-arch images on local dev machines (e.g., Apple Silicon).

## 2026-02-20: Automated Docs Publishing
- **Decision**: Implement GitHub Actions workflow to build and publish Antora site to GitLab Pages.
- **Rationale**: Automate documentation deployment to ensure it stays up-to-date with the code.
