# Trivy Analyzer Report

_Vulnerability scan results from Trivy._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"trivy"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/trivy_version"></a>**`trivy_version`** _(string, required)_
- <a id="properties/vulnerability_count"></a>**`vulnerability_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/critical_count"></a>**`critical_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/high_count"></a>**`high_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/medium_count"></a>**`medium_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/low_count"></a>**`low_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/unknown_count"></a>**`unknown_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/targets"></a>**`targets`** _(array, required)_
  - <a id="properties/targets/items"></a>**Items** _(object)_
    - <a id="properties/targets/items/properties/Target"></a>**`Target`** _(string, required)_
    - <a id="properties/targets/items/properties/Vulnerabilities"></a>**`Vulnerabilities`** _(array or null, required)_
      - <a id="properties/targets/items/properties/Vulnerabilities/items"></a>**Items** _(object)_
        - <a id="properties/targets/items/properties/Vulnerabilities/items/properties/VulnerabilityID"></a>**`VulnerabilityID`** _(string, required)_
        - <a id="properties/targets/items/properties/Vulnerabilities/items/properties/PkgName"></a>**`PkgName`** _(string, required)_
        - <a id="properties/targets/items/properties/Vulnerabilities/items/properties/InstalledVersion"></a>**`InstalledVersion`** _(string, required)_
        - <a id="properties/targets/items/properties/Vulnerabilities/items/properties/FixedVersion"></a>**`FixedVersion`** _(string)_
        - <a id="properties/targets/items/properties/Vulnerabilities/items/properties/Severity"></a>**`Severity`** _(string, required)_
        - <a id="properties/targets/items/properties/Vulnerabilities/items/properties/Title"></a>**`Title`** _(string)_
        - <a id="properties/targets/items/properties/Vulnerabilities/items/properties/Description"></a>**`Description`** _(string)_
