---
tags:
  - freshness
  - rules
---

# freshness-age

Image should be less than expected days old.

| Provider  | Level   | Tags      |
| :-------- | :------ | :-------- |
| freshness | warning | freshness |

## Parameters

| Name       | Default Value |
| :--------- | :------------ |
| `max_days` | `30`          |

## Messages

| Type     | Message                                                                                   |
| :------- | :---------------------------------------------------------------------------------------- |
| **Pass** | Image is less than ${rule.params.max_days} days old (${results.freshness.age_days} days). |
| **Fail** | Image is older than ${rule.params.max_days} days (${results.freshness.age_days} days).    |

## Playbook Example

```yaml
rules:
  freshness-age:
    params:
      max_days: 60
```

## Condition

```json
{
  "<": [
    {
      "var": "results.freshness.age_days"
    },
    {
      "var": "rule.params.max_days"
    }
  ]
}
```
