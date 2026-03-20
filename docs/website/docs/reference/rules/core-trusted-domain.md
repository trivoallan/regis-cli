---
tags:
  - core
  - rules
---

# core-trusted-domain

Image must originate from a trusted domain.

| Provider | Level    | Tags     |
| :------- | :------- | :------- |
| core     | critical | security |

## Parameters

| Name      | Default Value                                                 |
| :-------- | :------------------------------------------------------------ |
| `domains` | `['docker.io', 'registry-1.docker.io', 'quay.io', 'ghcr.io']` |

## Messages

| Type     | Message                                                          |
| :------- | :--------------------------------------------------------------- |
| **Pass** | Image originates from a trusted domain.                          |
| **Fail** | Image registry '${request.registry}' is not in the trusted list. |

## Playbook Example

```yaml
rules:
  core-trusted-domain:
    params:
      domains: ["my-registry.com"]
```

## Condition

```json
{
  "in": [
    {
      "var": "request.registry"
    },
    {
      "var": "rule.params.domains"
    }
  ]
}
```
