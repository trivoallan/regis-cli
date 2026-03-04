# Active Context

## Current Objective

Documentation update following the implementation of the MR description checklist feature.

## Recent Changes

- Added `integrations.gitlab.checklist` support to the playbook engine: items with an optional jsonLogic `condition` are evaluated at the end of `evaluate()` and exposed as `mr_description_checklist` in the result.
- Updated `playbook.schema.json` to include the `checklist` array definition under `integrations.gitlab`.
- Added example checklist items to `default.yaml` (three items including two conditional ones).
- Added `TestGitLabChecklist` unit tests (7 tests) in `test_playbook_engine.py` — all 24 tests pass.
- Updated `docs/modules/ROOT/pages/playbooks.adoc` with a new "GitLab Integration" section covering labels and the checklist feature.
- Updated `docs/modules/ROOT/pages/default-playbook.adoc` with a "GitLab Integrations" section documenting the default label and checklist configurations.
- Added support for a `hint` field on playbook sections to display explanatory text under section titles.
- Integrated GitHub Actions metadata (requester, workflow, run ID) into the template workflow for better traceability.
- Created comprehensive Cookiecutter usage guide in `docs/modules/ROOT/pages/cookiecutter.adoc`.
- Fixed Skopeo architecture mismatch error by skipping high-level `inspect` on image indexes.

## Next Steps

- Implement the CLI/GitLab layer that reads `mr_description_checklist` from the playbook result and appends Markdown checkboxes to the MR description.
