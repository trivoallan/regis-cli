# Active Context

## Current Objective
Initialize the project's documentation and fix security-related workflow permission issues.

## Recent Changes
- Fixed Docker permission issues by creating a home directory for the `regis` user (UID 1001), adjusting volume permissions in the workflow, and adding a fallback output mechanism in `cli.py`.
- Resolved `(MISSING)` scorecard values by exposing analyzer results at the root of the evaluation context in `engine.py`.
- Implemented dynamic filename logic for reports: prioritized by `html.filename` in scorecard, then scorecard basename, then fallback to `report.html`.
- Updated CLI to unconditionally generate a unified `report.json`, but generate distinct HTML files for each scorecard (e.g., `security.html`, `maturity.html`).
- Integrated GitHub Actions metadata (requester, workflow, run ID) into the template workflow for better traceability.
- Enhanced scorecard reports to display rule descriptions instead of technical names, improving readability.
- Created comprehensive Cookiecutter usage guide in `docs/modules/ROOT/pages/cookiecutter.adoc`.
- Fixed Skopeo architecture mismatch error by skipping high-level `inspect` on image indexes.
- Modified `.github/workflows/docker-publish.yml` to use least-privilege top-level permissions (`contents: read`).
- Modified `.github/workflows/releaser-pleaser.yml` to use least-privilege top-level permissions.
- Initialized Antora documentation structure in `docs/`.
- Created GitHub workflow integration guide in `docs/modules/ROOT/pages/github-workflow.adoc`.

## Next Steps
- Verify the documentation build process.
- Ensure all CI/CD workflows are functioning correctly.
