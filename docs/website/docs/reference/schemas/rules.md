# Rules definition

_Schema for regis-cli evaluating rules (rules.yaml)._

## Properties

- <a id="properties/rules"></a>**`rules`** _(array, required)_
  - <a id="properties/rules/items"></a>**Items** _(object)_
    - <a id="properties/rules/items/properties/slug"></a>**`slug`** _(string, required)_: Identifier for the rule.
    - <a id="properties/rules/items/properties/title"></a>**`title`** _(string, required)_: Human-readable title.
    - <a id="properties/rules/items/properties/level"></a>**`level`** _(string)_: Severity level of the rule. Must be one of: "critical", "warning", "info", or "none".
    - <a id="properties/rules/items/properties/tags"></a>**`tags`** _(array)_: Arbitrary tags to group rules.
      - <a id="properties/rules/items/properties/tags/items"></a>**Items** _(string)_
    - <a id="properties/rules/items/properties/enable"></a>**`enable`** _(boolean)_: Whether the rule is enabled. Defaults to true. Default: `true`.
    - <a id="properties/rules/items/properties/params"></a>**`params`** _(object)_: Configurable parameters for the rule condition. Can contain additional properties.
    - <a id="properties/rules/items/properties/messages"></a>**`messages`** _(object, required)_
      - <a id="properties/rules/items/properties/messages/properties/pass"></a>**`pass`** _(string, required)_: Message rendered when rule passes.
      - <a id="properties/rules/items/properties/messages/properties/fail"></a>**`fail`** _(string, required)_: Message rendered when rule fails.
    - <a id="properties/rules/items/properties/condition"></a>**`condition`** _(object, required)_: JsonLogic condition evaluated against the flattened analysis report.
