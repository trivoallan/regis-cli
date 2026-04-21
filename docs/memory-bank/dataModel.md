# Data Model

## Entity Relationships
- Registry image data flows into analyzer outputs.
- Analyzer outputs feed playbook evaluation.
- Playbook results feed report generation.

## Database Schema
No database schema was identified in the inspected files.

## Data Flow
1. Fetch registry metadata.
2. Run analyzer checks.
3. Validate outputs against schemas.
4. Evaluate policy rules.
5. Render reports and artifacts.

## Migrations
No migrations were identified in the inspected files.

## Data Constraints
- Analyzer payloads must match JSON schemas.
- Rule evaluation inputs should be deterministic.
- Security and compliance outputs should preserve source evidence.
