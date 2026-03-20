---
tags:
  - trivy
  - rules
---

# trivy-no-high

No HIGH vulnerabilities found by Trivy.

| Provider | Level   | Tags     |
| :------- | :------ | :------- |
| trivy    | warning | security |

## Parameters

| Name        | Default Value |
| :---------- | :------------ |
| `max_count` | `0`           |

## Messages

| Type     | Message                                                                                  |
| :------- | :--------------------------------------------------------------------------------------- |
| **Pass** | No high vulnerabilities detected.                                                        |
| **Fail** | Image has ${results.trivy.high_count} high CVEs (max allowed: ${rule.params.max_count}). |

## Playbook Example

```yaml
rules:
  trivy-no-high:
    params:
      max_count: 3
```

## Condition

```json
{
  "<=": [
    {
      "var": "results.trivy.high_count"
    },
    {
      "var": "rule.params.max_count"
    }
  ]
}
```
