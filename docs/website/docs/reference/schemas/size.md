# Size Analyzer Report

_Image size breakdown._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"size"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/multi_arch"></a>**`multi_arch`** _(boolean, required)_
- <a id="properties/total_compressed_bytes"></a>**`total_compressed_bytes`** _(integer, required)_: Minimum: `0`.
- <a id="properties/total_compressed_human"></a>**`total_compressed_human`** _(string, required)_
- <a id="properties/layer_count"></a>**`layer_count`** _(integer, required)_: Minimum: `0`.
- <a id="properties/config_size_bytes"></a>**`config_size_bytes`** _(integer, required)_: Minimum: `0`.
- <a id="properties/layers"></a>**`layers`** _(array, required)_
  - <a id="properties/layers/items"></a>**Items** _(object)_: Cannot contain additional properties.
    - <a id="properties/layers/items/properties/index"></a>**`index`** _(integer, required)_: Minimum: `0`.
    - <a id="properties/layers/items/properties/digest"></a>**`digest`** _(string, required)_
    - <a id="properties/layers/items/properties/size_bytes"></a>**`size_bytes`** _(integer, required)_: Minimum: `0`.
    - <a id="properties/layers/items/properties/size_human"></a>**`size_human`** _(string, required)_
- <a id="properties/platforms"></a>**`platforms`** _(array or null, required)_
  - <a id="properties/platforms/items"></a>**Items** _(object)_: Cannot contain additional properties.
    - <a id="properties/platforms/items/properties/platform"></a>**`platform`** _(string, required)_
    - <a id="properties/platforms/items/properties/compressed_bytes"></a>**`compressed_bytes`** _(integer, required)_: Minimum: `0`.
    - <a id="properties/platforms/items/properties/compressed_human"></a>**`compressed_human`** _(string, required)_
    - <a id="properties/platforms/items/properties/layer_count"></a>**`layer_count`** _(integer, required)_: Minimum: `0`.
