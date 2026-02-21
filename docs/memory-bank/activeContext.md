# Active Context

## Current Objective
Implement the `version` command in the CLI and ensure all tests are up to date.

## Recent Changes
- Added a `version` command to the CLI to display the current package version.
- Refactored `importlib.metadata` imports in `cli.py` for better organization.
- Fixed an outdated test case in `test_cli.py` that used defunct CLI options.
- Fixed Docker permission issues by creating a home directory for the `regis` user (UID 1001), adjusting volume permissions in the workflow, and adding a fallback output mechanism in `cli.py`.
- Resolved `(MISSING)` playbook values by exposing analyzer results at the root of the evaluation context in `engine.py`.
- Implemented dynamic filename logic for reports: prioritized by `html.filename` in playbook, then playbook basename, then fallback to `report.html`.
- Updated CLI to unconditionally generate a unified `report.json`, but generate distinct HTML files for each playbook (e.g., `security.html`, `maturity.html`).
- Added support for a `hint` field on playbook sections to display explanatory text under section titles.
- Integrated GitHub Actions metadata (requester, workflow, run ID) into the template workflow for better traceability.
- Enhanced playbook reports to display rule descriptions instead of technical names, improving readability.
- Created comprehensive Cookiecutter usage guide in `docs/modules/ROOT/pages/cookiecutter.adoc`.
- Fixed Skopeo architecture mismatch error by skipping high-level `inspect` on image indexes.
- Modified `.github/workflows/docker-publish.yml` to use least-privilege top-level permissions (`contents: read`).
- Modified `.github/workflows/releaser-pleaser.yml` to use least-privilege top-level permissions.
- Initialized Antora documentation structure in `docs/`.
- Created GitHub workflow integration guide in `docs/modules/ROOT/pages/github-workflow.adoc`.

## Next Steps
- Verify the documentation build process.
- Ensure all CI/CD workflows are functioning correctly.
