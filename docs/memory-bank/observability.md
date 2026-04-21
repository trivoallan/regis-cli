# Observability

## Logging

- CLI and workflow outputs appear to rely on standard Python logging and job logs.

## Monitoring

- CI workflows provide the main operational visibility
- Coverage badges and generated artifacts are used as quality signals

## Tracing

- No distributed tracing setup was identified in the inspected files

## Alerting

| Alert      | Condition                                         | Severity | Channel                              |
| ---------- | ------------------------------------------------- | -------- | ------------------------------------ |
| CI failure | Test, lint, security, or release workflow failure | High     | GitHub/GitLab workflow notifications |

## Health Checks

- Not documented in the inspected files

## Error Tracking

- No dedicated error-tracking service was identified in the inspected files
