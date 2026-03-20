# regis-cli Analysis Report

_Final report envelope produced by regis-cli, containing request metadata and analyzer results._

## Properties

- <a id="properties/version"></a>**`version`** _(string or null, required)_: Version of regis-cli that generated this report.
- <a id="properties/tier"></a>**`tier`** _(string or null)_: The earned tier (e.g. Gold, Silver, Bronze) based on playbook conditions.
- <a id="properties/badges"></a>**`badges`** _(array)_
  - <a id="properties/badges/items"></a>**Items** _(object)_
    - <a id="properties/badges/items/properties/slug"></a>**`slug`** _(string)_
    - <a id="properties/badges/items/properties/scope"></a>**`scope`** _(string, required)_
    - <a id="properties/badges/items/properties/value"></a>**`value`** _(string or null)_
    - <a id="properties/badges/items/properties/class"></a>**`class`** _(string, required)_: Must be one of: "success", "warning", "error", or "information".
    - <a id="properties/badges/items/properties/label"></a>**`label`** _(string)_
- <a id="properties/metadata"></a>**`metadata`** _(object)_: Arbitrary user-provided metadata. Can contain additional properties.
- <a id="properties/links"></a>**`links`** _(array)_: Custom templated links.
  - <a id="properties/links/items"></a>**Items** _(object)_
    - <a id="properties/links/items/properties/label"></a>**`label`** _(string, required)_
    - <a id="properties/links/items/properties/url"></a>**`url`** _(string, required)_
- <a id="properties/request"></a>**`request`** _(object, required)_: Metadata describing the analysis request. Cannot contain additional properties.
  - <a id="properties/request/properties/url"></a>**`url`** _(string, required)_: Original URL or image reference provided by the user.
  - <a id="properties/request/properties/registry"></a>**`registry`** _(string, required)_: Resolved registry hostname (e.g. registry-1.docker.io).
  - <a id="properties/request/properties/repository"></a>**`repository`** _(string, required)_: Full repository path (e.g. library/nginx).
  - <a id="properties/request/properties/tag"></a>**`tag`** _(string, required)_: Image tag that was analyzed.
  - <a id="properties/request/properties/digest"></a>**`digest`** _(string)_: Resolved image manifest digest (e.g. sha256-xxx), if available.
  - <a id="properties/request/properties/analyzers"></a>**`analyzers`** _(array, required)_: List of analyzer names that were executed.
    - <a id="properties/request/properties/analyzers/items"></a>**Items** _(string)_
  - <a id="properties/request/properties/timestamp"></a>**`timestamp`** _(string, format: date-time, required)_: ISO 8601 UTC timestamp of the analysis.
  - <a id="properties/request/properties/metadata"></a>**`metadata`** _(object)_: Arbitrary user-provided metadata. Can contain additional properties.
- <a id="properties/results"></a>**`results`** _(object, required)_: Analyzer results keyed by analyzer name. Can contain additional properties.
  - <a id="properties/results/additionalProperties"></a>**Additional properties** _(object)_
- <a id="properties/playbooks"></a>**`playbooks`** _(array)_: List of evaluated playbook results.
  - <a id="properties/playbooks/items"></a>**Items**: Refer to _[playbook_result.schema.json](:///playbook_result.schema.json#)_.
- <a id="properties/playbook"></a>**`playbook`**: Primary playbook result (shorthand for playbooks[0]). Refer to _[playbook_result.schema.json](:///playbook_result.schema.json#)_.
- <a id="properties/rules"></a>**`rules`** _(array)_: List of unified rule results (promoted from playbooks[0]).
  - <a id="properties/rules/items"></a>**Items** _(object)_
    - <a id="properties/rules/items/properties/slug"></a>**`slug`** _(string, required)_
    - <a id="properties/rules/items/properties/title"></a>**`title`** _(string, required)_
    - <a id="properties/rules/items/properties/level"></a>**`level`** _(string)_
    - <a id="properties/rules/items/properties/tags"></a>**`tags`** _(array)_
      - <a id="properties/rules/items/properties/tags/items"></a>**Items** _(string)_
    - <a id="properties/rules/items/properties/passed"></a>**`passed`** _(boolean, required)_
    - <a id="properties/rules/items/properties/status"></a>**`status`** _(string, required)_: Must be one of: "passed", "failed", or "incomplete".
    - <a id="properties/rules/items/properties/message"></a>**`message`** _(string, required)_
    - <a id="properties/rules/items/properties/analyzers"></a>**`analyzers`** _(array)_
      - <a id="properties/rules/items/properties/analyzers/items"></a>**Items** _(string)_
- <a id="properties/rules_summary"></a>**`rules_summary`** _(object)_: Summary of rule evaluation results.
  - <a id="properties/rules_summary/properties/score"></a>**`score`** _(integer)_: Minimum: `0`. Maximum: `100`.
  - <a id="properties/rules_summary/properties/total"></a>**`total`** _(array)_
    - <a id="properties/rules_summary/properties/total/items"></a>**Items** _(string)_
  - <a id="properties/rules_summary/properties/passed"></a>**`passed`** _(array)_
    - <a id="properties/rules_summary/properties/passed/items"></a>**Items** _(string)_
  - <a id="properties/rules_summary/properties/by_tag"></a>**`by_tag`** _(object)_: Can contain additional properties.
    - <a id="properties/rules_summary/properties/by_tag/additionalProperties"></a>**Additional properties** _(object)_
      - <a id="properties/rules_summary/properties/by_tag/additionalProperties/properties/rules"></a>**`rules`** _(array, required)_
        - <a id="properties/rules_summary/properties/by_tag/additionalProperties/properties/rules/items"></a>**Items** _(string)_
      - <a id="properties/rules_summary/properties/by_tag/additionalProperties/properties/passed_rules"></a>**`passed_rules`** _(array, required)_
        - <a id="properties/rules_summary/properties/by_tag/additionalProperties/properties/passed_rules/items"></a>**Items** _(string)_
      - <a id="properties/rules_summary/properties/by_tag/additionalProperties/properties/score"></a>**`score`** _(integer, required)_: Minimum: `0`. Maximum: `100`.
