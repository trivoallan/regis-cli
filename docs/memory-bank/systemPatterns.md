# System Patterns

## Architecture
`regis-cli` follows a modular, pluggable architecture.

### Key Components
- **CLI (Click)**: Entry point for user interaction.
- **Engine**: Orchestrates analysis and scorecard evaluation.
- **Analyzers**: Pluggable modules that extract specific data (e.g., Skopeo, Trivy, Hadolint).
- **Scorecard Engine**: Evaluates JSON logic rules against analyzer results.
- **Report Generators**: Produces output in various formats using Jinja2 templates.

## Rules and Standards
- **Python**: Use `pipenv` for dependency management.
- **CI/CD**: GitHub Actions with Release Please and Trunk.
- **Documentation**: Antora for documentation as code.
- **Aesthetics**: High priority on visual excellence for HTML reports.
