---
tags:
  - hadolint
  - rules
---

# hadolint.severity-count

Fails if the number of issues for a given severity level exceeds the maximum allowed count. This is a reusable rule template.

| Provider                                  | Level    | Tags           |
| :---------------------------------------- | :------- | :------------- |
| [hadolint](/reference/analyzers/hadolint) | Variable | Best practices |

## Parameters

| Name        | Default Value | Description                                                    |
| :---------- | :------------ | :------------------------------------------------------------- |
| `level`     | `error`       | Severity level to check (`error`, `warning`, `info`, `style`). |
| `max_count` | `0`           | Maximum allowed issues of this level.                          |

## Messages

| Type     | Message                                                                                                                                      |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pass** | Hadolint ${rule.params.level} issues are within limits.                                                                                      |
| **Fail** | Hadolint found ${results.hadolint.issues_by_level.${rule.params.level}} ${rule.params.level} issues (max allowed: ${rule.params.max_count}). |

## Playbook Example

```yaml
rules:
  - provider: hadolint
    rule: severity-count
    options:
      level: error
      max_count: 0
    level: critical

  - provider: hadolint
    rule: severity-count
    options:
      level: warning
      max_count: 5
    level: warning
```

## Condition

```json
{
  "<=": [
    {
      "get": [
        { "var": "results.hadolint.issues_by_level" },
        { "var": "rule.params.level" }
      ]
    },
    {
      "var": "rule.params.max_count"
    }
  ]
}
```
