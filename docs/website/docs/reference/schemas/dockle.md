# Dockle Analyzer Report

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"dockle"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/error"></a>**`error`** _(string)_: Any error encountered during execution.
- <a id="properties/passed"></a>**`passed`** _(boolean, required)_: True if no issues were found, False otherwise.
- <a id="properties/issues_count"></a>**`issues_count`** _(integer, required)_: Total number of issues found.
- <a id="properties/issues_by_level"></a>**`issues_by_level`** _(object, required)_: Count of issues grouped by severity level. Cannot contain additional properties.
  - <a id="properties/issues_by_level/properties/FATAL"></a>**`FATAL`** _(integer)_: Default: `0`.
  - <a id="properties/issues_by_level/properties/WARN"></a>**`WARN`** _(integer)_: Default: `0`.
  - <a id="properties/issues_by_level/properties/INFO"></a>**`INFO`** _(integer)_: Default: `0`.
  - <a id="properties/issues_by_level/properties/SKIP"></a>**`SKIP`** _(integer)_: Default: `0`.
  - <a id="properties/issues_by_level/properties/PASS"></a>**`PASS`** _(integer)_: Default: `0`.
- <a id="properties/issues"></a>**`issues`** _(array, required)_: List of issues found by Dockle.
  - <a id="properties/issues/items"></a>**Items** _(object)_
    - <a id="properties/issues/items/properties/code"></a>**`code`** _(string, required)_: Dockle rule code (e.g., CIS-DI-0001).
    - <a id="properties/issues/items/properties/title"></a>**`title`** _(string, required)_: Short description of the rule.
    - <a id="properties/issues/items/properties/level"></a>**`level`** _(string, required)_: Severity level of the issue. Must be one of: "FATAL", "WARN", "INFO", "SKIP", or "PASS".
    - <a id="properties/issues/items/properties/alerts"></a>**`alerts`** _(array, required)_: Specific details or files related to the issue.
      - <a id="properties/issues/items/properties/alerts/items"></a>**Items** _(string)_
