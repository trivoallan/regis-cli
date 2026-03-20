# Hadolint Analyzer Report

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"hadolint"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/error"></a>**`error`** _(string)_: Any error encountered during execution.
- <a id="properties/passed"></a>**`passed`** _(boolean, required)_: True if no issues were found, False otherwise.
- <a id="properties/issues_count"></a>**`issues_count`** _(integer, required)_: Total number of issues found.
- <a id="properties/issues_by_level"></a>**`issues_by_level`** _(object, required)_: Count of issues grouped by severity level. Cannot contain additional properties.
  - <a id="properties/issues_by_level/properties/error"></a>**`error`** _(integer)_: Default: `0`.
  - <a id="properties/issues_by_level/properties/warning"></a>**`warning`** _(integer)_: Default: `0`.
  - <a id="properties/issues_by_level/properties/info"></a>**`info`** _(integer)_: Default: `0`.
  - <a id="properties/issues_by_level/properties/style"></a>**`style`** _(integer)_: Default: `0`.
- <a id="properties/issues"></a>**`issues`** _(array, required)_: List of issues found by Hadolint.
  - <a id="properties/issues/items"></a>**Items** _(object)_
    - <a id="properties/issues/items/properties/code"></a>**`code`** _(string, required)_: Hadolint rule code (e.g., DL3008).
    - <a id="properties/issues/items/properties/level"></a>**`level`** _(string, required)_: Severity level of the issue. Must be one of: "error", "warning", "info", or "style".
    - <a id="properties/issues/items/properties/message"></a>**`message`** _(string, required)_: Description of the issue.
    - <a id="properties/issues/items/properties/line"></a>**`line`** _(integer or null)_: Line number in the pseudo-Dockerfile.
