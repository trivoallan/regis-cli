---
tags:
  - trivy
  - rules
---

# trivy-no-critical

No CRITICAL vulnerabilities found by Trivy.

| Provider | Level    | Tags     |
| :------- | :------- | :------- |
| trivy    | critical | security |

## Parameters

| Name        | Default Value |
| :---------- | :------------ |
| `max_count` | `0`           |

## Messages

| Type     | Message                                                                                          |
| :------- | :----------------------------------------------------------------------------------------------- |
| **Pass** | No critical vulnerabilities detected.                                                            |
| **Fail** | Image has ${results.trivy.critical_count} critical CVEs (max allowed: ${rule.params.max_count}). |

## Playbook Example

```yaml
rules:
  trivy-no-critical:
    params:
      max_count: 0
```

## Condition

```json
{
  "<=": [
    {
      "var": "results.trivy.critical_count"
    },
    {
      "var": "rule.params.max_count"
    }
  ]
}
```
