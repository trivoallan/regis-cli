---
tags:
  - skopeo
  - rules
---

# skopeo-required-labels

Image must have required OCI labels.

| Provider | Level   | Tags     |
| :------- | :------ | :------- |
| skopeo   | warning | metadata |

## Parameters

| Name     | Default Value                         |
| :------- | :------------------------------------ |
| `labels` | `['org.opencontainers.image.source']` |

## Messages

| Type     | Message                                                              |
| :------- | :------------------------------------------------------------------- |
| **Pass** | All required labels are present.                                     |
| **Fail** | Image is missing one or more required labels: ${rule.params.labels}. |

## Playbook Example

```yaml
rules:
  skopeo-required-labels:
    params:
      labels:
        ["org.opencontainers.image.source", "org.opencontainers.image.vendor"]
```

## Condition

```json
{
  "contains_all": [
    {
      "keys": [
        {
          "var": "results.skopeo.platforms.0.labels"
        }
      ]
    },
    {
      "var": "rule.params.labels"
    }
  ]
}
```
