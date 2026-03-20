---
tags:
  - dockle
  - rules
---

# dockle.severity-count

Fails if the number of issues for a given severity level exceeds the maximum allowed count. This is a reusable rule template.

| Provider                              | Level    | Tags     |
| :------------------------------------ | :------- | :------- |
| [dockle](/reference/analyzers/dockle) | Variable | Security |

## Parameters

| Name        | Default Value | Description                                        |
| :---------- | :------------ | :------------------------------------------------- |
| `level`     | `FATAL`       | Severity level to check (`FATAL`, `WARN`, `INFO`). |
| `max_count` | `0`           | Maximum allowed issues of this level.              |

## Messages

| Type     | Message                                                                                                                                  |
| :------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Pass** | Dockle ${rule.params.level} issues are within limits.                                                                                    |
| **Fail** | Dockle found ${results.dockle.issues_by_level.${rule.params.level}} ${rule.params.level} issues (max allowed: ${rule.params.max_count}). |

## Playbook Example

```yaml
rules:
  - provider: dockle
    rule: severity-count
    options:
      level: FATAL
      max_count: 0
    level: critical

  - provider: dockle
    rule: severity-count
    options:
      level: WARN
      max_count: 3
    level: warning
```

## Condition

```json
{
  "<=": [
    {
      "get": [
        { "var": "results.dockle.issues_by_level" },
        { "var": "rule.params.level" }
      ]
    },
    {
      "var": "rule.params.max_count"
    }
  ]
}
```
