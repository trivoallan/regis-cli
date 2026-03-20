# SBOM Analyzer Report

_Software Bill of Materials extracted from a container image using Trivy (CycloneDX)._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"sbom"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/has_sbom"></a>**`has_sbom`** _(boolean, required)_
- <a id="properties/sbom_format"></a>**`sbom_format`** _(string, required)_
- <a id="properties/sbom_version"></a>**`sbom_version`** _(string, required)_
- <a id="properties/total_components"></a>**`total_components`** _(integer, required)_: Minimum: `0`.
- <a id="properties/component_types"></a>**`component_types`** _(object, required)_: Count of components grouped by type (library, application, framework, …). Can contain additional properties.
  - <a id="properties/component_types/additionalProperties"></a>**Additional properties** _(integer)_: Minimum: `0`.
- <a id="properties/total_dependencies"></a>**`total_dependencies`** _(integer, required)_: Minimum: `0`.
- <a id="properties/licenses"></a>**`licenses`** _(array, required)_: Sorted unique license identifiers found across all components.
  - <a id="properties/licenses/items"></a>**Items** _(string)_
- <a id="properties/components"></a>**`components`** _(array, required)_
  - <a id="properties/components/items"></a>**Items** _(object)_: Cannot contain additional properties.
    - <a id="properties/components/items/properties/name"></a>**`name`** _(string, required)_
    - <a id="properties/components/items/properties/version"></a>**`version`** _(string or null)_
    - <a id="properties/components/items/properties/type"></a>**`type`** _(string, required)_
    - <a id="properties/components/items/properties/purl"></a>**`purl`** _(string or null)_
    - <a id="properties/components/items/properties/licenses"></a>**`licenses`** _(array)_
      - <a id="properties/components/items/properties/licenses/items"></a>**Items** _(string)_
