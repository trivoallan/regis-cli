# Versioning Analyzer Report

_Report analyzing tag naming conventions and semver adoption._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"versioning"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/total_tags"></a>**`total_tags`** _(integer, required)_: Minimum: `0`.
- <a id="properties/dominant_pattern"></a>**`dominant_pattern`** _(string, required)_: Must be one of: "semver", "semver-prerelease", "semver-variant", "calver", "numeric", "hash", "named", or "unknown".
- <a id="properties/release_lines"></a>**`release_lines`** _(array)_
  - <a id="properties/release_lines/items"></a>**Items** _(string)_
- <a id="properties/semver_compliant_percentage"></a>**`semver_compliant_percentage`** _(number, required)_: Minimum: `0`. Maximum: `100`.
- <a id="properties/patterns"></a>**`patterns`** _(array, required)_
  - <a id="properties/patterns/items"></a>**Items** _(object)_: Cannot contain additional properties.
    - <a id="properties/patterns/items/properties/pattern"></a>**`pattern`** _(string, required)_: Must be one of: "semver", "semver-prerelease", "semver-variant", "calver", "numeric", "hash", or "named".
    - <a id="properties/patterns/items/properties/count"></a>**`count`** _(integer, required)_: Minimum: `0`.
    - <a id="properties/patterns/items/properties/percentage"></a>**`percentage`** _(number, required)_: Minimum: `0`. Maximum: `100`.
    - <a id="properties/patterns/items/properties/examples"></a>**`examples`** _(array, required)_: Length must be at most 10.
      - <a id="properties/patterns/items/properties/examples/items"></a>**Items** _(string)_
- <a id="properties/variants"></a>**`variants`** _(array, required)_
  - <a id="properties/variants/items"></a>**Items** _(object)_: Cannot contain additional properties.
    - <a id="properties/variants/items/properties/name"></a>**`name`** _(string, required)_
    - <a id="properties/variants/items/properties/count"></a>**`count`** _(integer, required)_: Minimum: `0`.
    - <a id="properties/variants/items/properties/percentage"></a>**`percentage`** _(number, required)_: Minimum: `0`. Maximum: `100`.
    - <a id="properties/variants/items/properties/examples"></a>**`examples`** _(array, required)_: Length must be at most 10.
      - <a id="properties/variants/items/properties/examples/items"></a>**Items** _(string)_
