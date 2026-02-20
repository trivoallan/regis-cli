# System Patterns

## Analysis Flow
1. **Trigger**: GitHub Actions push/schedule or manual dispatch.
2. **Analysis**: `regis-cli` runs via Docker.
3. **Evaluation**: Scorecards are applied to the analysis results.
4. **Reporting**: JSON and HTML reports are generated and stored as artifacts.

## File Structure
- `.github/workflows/`: CI/CD definitions.
- `scorecards/`: Security policy definitions.
- `reports/`: (Generated) Analysis output.
- `docs/memory-bank/`: Project context and progress.
