# Fix Broken Documentation Examples & Add Versioning

## Context

The Alpine playbook example at `https://trivoallan.github.io/regis/docs/examples/playbooks/default/alpine/` is broken due to a baseUrl mismatch. The generated report HTML was built with baseUrl="/" (default) instead of the correct path for deployment.

Additionally, examples should be versioned to align with Docusaurus versioned docs, with examples regenerated at release time as part of the Release Please workflow.

## Root Cause Analysis

1. **Broken Link**: The generated report uses `pathname:///regis/examples/...` but should use `/regis/docs/examples/...` to match the main docs baseUrl
2. **BaseUrl Mismatch**: Report viewer built with default baseUrl="/" instead of the correct deployment path
3. **Missing Versioning**: Examples exist only in `/static/examples/` (unversioned) and aren't regenerated at release time
4. **Release Workflow Gap**: No step in CI/Release Please to regenerate examples during version releases

## Implementation Plan

### Phase 1: Fix Current Broken Example
**Goal**: Regenerate the Alpine example with correct baseUrl

**Steps**:
1. Regenerate the Alpine example with explicit `--base-url` parameter:
   ```bash
   pipenv run regis analyze alpine:latest \
     --evaluate --site \
     --base-url "/regis/examples/playbooks/default/alpine/" \
     --output-dir docs/website/static/examples/playbooks/default/alpine
   ```
   
2. Verify the generated HTML at `docs/website/static/examples/playbooks/default/alpine/index.html` shows correct baseUrl in error banner

3. Test the link in `docs/website/docs/reference/playbooks/default/examples/alpine.md` works correctly

**Files to modify**:
- `docs/website/static/examples/playbooks/default/alpine/` — regenerated output
- Potentially `alpine.md` if the pathname URL needs adjustment

### Phase 2: Add Versioning Infrastructure
**Goal**: Create versioned examples structure and documentation

**Steps**:
1. Create script: `scripts/generate_examples.sh`
   - Generates all playbook examples (alpine, regis-cli, etc.)
   - Takes version name as parameter (e.g., "1.0.0" or "main")
   - Uses correct baseUrl based on version:
     - Main/edge: `/regis/examples/playbooks/...`
     - Versioned: `/regis/docs/version-X.Y.Z/examples/playbooks/...`

2. Update `docs/website/docusaurus.config.ts`:
   - Ensure versioning config is correct
   - Verify baseUrl settings for versioned docs

3. Create version-specific example markdown files:
   - Mirror structure from `docs/website/docs/reference/playbooks/` to `docs/website/versioned_docs/version-X.Y.Z/reference/playbooks/`
   - Example links will auto-resolve to correct versioned paths

### Phase 3: Integrate into Release Workflow
**Goal**: Regenerate examples at release time

**Steps**:
1. Add GitHub Actions workflow step in release process:
   - Trigger after Release Please creates version tag
   - Run example generation script for the new version
   - Commit regenerated examples to the release branch

2. Update `.release-please-manifest.json` or Release Please config if needed to support this workflow

**Files to create/modify**:
- `.github/workflows/release.yml` or similar — add example generation step
- `scripts/generate_examples.sh` — the example generation script

### Phase 4: Verification
**Goal**: Ensure all examples work correctly

1. **Immediate verification** (Phase 1):
   - Run regeneration command locally
   - Verify Alpine example loads at the deployed URL
   - Check baseUrl error banner shows correct path

2. **Integration verification** (Phase 2-3):
   - Build docs locally: `cd docs/website && pnpm build`
   - Verify versioned examples are included in build output
   - Test example links in both main and versioned docs resolve correctly
   - Simulate release workflow by running example generation for a test version

3. **Regression check**:
   - Verify no other broken example links exist
   - Search docs for other `pathname:///regis/examples/` references

## Critical Files

**Current Example Documentation**:
- `docs/website/docs/reference/playbooks/default/examples/alpine.md` — contains broken link
- `docs/website/static/examples/playbooks/default/alpine/` — generated output directory

**Report Generation Code**:
- `regis/utils/report.py` — handles report generation
- `regis/report/docusaurus.py` — manages Docusaurus report viewer build
- `apps/report-viewer/docusaurus.config.ts` — baseUrl configuration

**Documentation Configuration**:
- `docs/website/docusaurus.config.ts` — main docs baseUrl and versioning config
- `docs/website/versioned_docs/` — where versioned examples should go

**Release Configuration**:
- `.github/workflows/` — release and CI workflows
- Release Please manifest/config

## Known Dependencies

- `regis analyze` command accepts `--base-url` parameter
- Report viewer app uses `REPORT_BASE_URL` env var (or hardcoded fallback)
- Docusaurus handles versioning via `versioned_docs/` and `versions.json`

## Success Criteria

1. Alpine example loads without error at deployed URL
2. Example links work in both main and versioned documentation
3. Release workflow automatically regenerates examples for each version
4. No 404 errors on example documentation pages
