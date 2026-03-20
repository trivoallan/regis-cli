---
tags:
  - skopeo
  - rules
---

# skopeo-no-root

Image must not run as root.

| Provider | Level    | Tags     |
| :------- | :------- | :------- |
| skopeo   | critical | security |

## Parameters

| Name             | Default Value |
| :--------------- | :------------ |
| `forbidden_user` | `root`        |

## Messages

| Type     | Message                                                     |
| :------- | :---------------------------------------------------------- |
| **Pass** | Image does not run as '${rule.params.forbidden_user}'.      |
| **Fail** | Image configured to run as '${rule.params.forbidden_user}'. |

## Playbook Example

```yaml
rules:
  skopeo-no-root:
    params:
      forbidden_user: non-root-user
```

## Condition

```json
{
  "!=": [
    {
      "var": "results.skopeo.platforms.0.user"
    },
    {
      "var": "rule.params.forbidden_user"
    }
  ]
}
```
