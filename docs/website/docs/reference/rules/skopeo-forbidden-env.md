---
tags:
  - skopeo
  - rules
---

# skopeo-forbidden-env

Image must not contain forbidden environment variables.

| Provider | Level    | Tags     |
| :------- | :------- | :------- |
| skopeo   | critical | security |

## Parameters

| Name   | Default Value             |
| :----- | :------------------------ |
| `keys` | `['DEBUG', 'SECRET_KEY']` |

## Messages

| Type     | Message                                                     |
| :------- | :---------------------------------------------------------- |
| **Pass** | No forbidden environment variables found.                   |
| **Fail** | Image contains one or more forbidden environment variables. |

## Playbook Example

```yaml
rules:
  skopeo-forbidden-env:
    params:
      keys: ["DEBUG", "SECRET_KEY", "DATABASE_URL"]
```

## Condition

```json
{
  "!": {
    "env_contains": [
      {
        "var": "results.skopeo.platforms.0.env"
      },
      {
        "var": "rule.params.keys"
      }
    ]
  }
}
```
