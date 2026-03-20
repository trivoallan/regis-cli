---
tags:
  - trivy
  - rules
---

# trivy-secret-scan

No secrets or credentials should be embedded in the image.

| Provider | Level    | Tags     |
| :------- | :------- | :------- |
| trivy    | critical | security |

## Parameters

| Name        | Default Value |
| :---------- | :------------ |
| `max_count` | `0`           |

## Messages

| Type     | Message                                                                            |
| :------- | :--------------------------------------------------------------------------------- |
| **Pass** | No secrets detected in the image.                                                  |
| **Fail** | Trivy detected ${results.trivy.secrets_count} secrets or credentials in the image. |

## Playbook Example

```yaml
rules:
  trivy-secret-scan:
    params:
      max_count: 0
```

## Condition

```json
{
  "<=": [
    {
      "var": "results.trivy.secrets_count"
    },
    {
      "var": "rule.params.max_count"
    }
  ]
}
```
