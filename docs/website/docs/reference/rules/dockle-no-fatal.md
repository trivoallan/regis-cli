---
tags:
  - dockle
  - rules
---

# dockle-no-fatal

No FATAL issues found by Dockle.

| Provider | Level    | Tags     |
| :------- | :------- | :------- |
| dockle   | critical | security |

## Parameters

| Name        | Default Value |
| :---------- | :------------ |
| `max_count` | `0`           |

## Messages

| Type     | Message                                                                                                    |
| :------- | :--------------------------------------------------------------------------------------------------------- |
| **Pass** | Image has no critical CVEs.                                                                                |
| **Fail** | Dockle found ${results.dockle.issues_by_level.FATAL} fatal issues (max allowed: ${rule.params.max_count}). |

## Playbook Example

```yaml
rules:
  dockle-no-fatal:
    params:
      max_count: 0
```

## Condition

```json
{
  "<=": [
    {
      "var": "results.dockle.issues_by_level.FATAL"
    },
    {
      "var": "rule.params.max_count"
    }
  ]
}
```
