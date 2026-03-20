---
tags:
  - skopeo
  - rules
---

# skopeo-tag-not-latest

Image tag should not be 'latest'.

| Provider | Level   | Tags      |
| :------- | :------ | :-------- |
| skopeo   | warning | lifecycle |

## Messages

| Type     | Message                                                              |
| :------- | :------------------------------------------------------------------- |
| **Pass** | Image tag is not 'latest'.                                           |
| **Fail** | Image is using the 'latest' tag. Use immutable version tags instead. |

## Playbook Example

```yaml
rules:
  skopeo-tag-not-latest: {}
```

## Condition

```json
{
  "!=": [
    {
      "var": "request.tag"
    },
    "latest"
  ]
}
```
