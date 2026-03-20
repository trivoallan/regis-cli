# Provenance Analyzer Report

_Build provenance and supply-chain attestation information._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"provenance"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/has_provenance"></a>**`has_provenance`** _(boolean, required)_
- <a id="properties/has_cosign_signature"></a>**`has_cosign_signature`** _(boolean, required)_
- <a id="properties/source_tracked"></a>**`source_tracked`** _(boolean, required)_
- <a id="properties/indicators_count"></a>**`indicators_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/indicators"></a>**`indicators`** _(array, required)_
  - <a id="properties/indicators/items"></a>**Items** _(object)_: Cannot contain additional properties.
    - <a id="properties/indicators/items/properties/type"></a>**`type`** _(string, required)_
    - <a id="properties/indicators/items/properties/key"></a>**`key`** _(string, required)_
    - <a id="properties/indicators/items/properties/value"></a>**`value`** _(string, required)_
