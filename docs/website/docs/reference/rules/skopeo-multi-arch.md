---
tags:
  - skopeo
  - rules
---

# skopeo-multi-arch

Image should support multiple platforms.

| Provider | Level | Tags          |
| :------- | :---- | :------------ |
| skopeo   | info  | compatibility |

## Parameters

| Name            | Default Value |
| :-------------- | :------------ |
| `min_platforms` | `2`           |

## Messages

| Type     | Message                                                                                                        |
| :------- | :------------------------------------------------------------------------------------------------------------- |
| **Pass** | Image supports ${results.skopeo.platforms.length} platforms.                                                   |
| **Fail** | Image only supports ${results.skopeo.platforms.length} platforms (min required: ${rule.params.min_platforms}). |

## Playbook Example

```yaml
rules:
  skopeo-multi-arch:
    params:
      min_platforms: 1
```

## Condition

```json
{
  ">=": [
    {
      "reduce": [
        {
          "var": "results.skopeo.platforms"
        },
        {
          "+": [
            1,
            {
              "var": "accumulator"
            }
          ]
        },
        0
      ]
    },
    {
      "var": "rule.params.min_platforms"
    }
  ]
}
```
