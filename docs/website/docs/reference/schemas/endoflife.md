# End-of-Life Analyzer Report

_Report containing lifecycle information from endoflife.date._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"endoflife"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/product"></a>**`product`** _(string, required)_: Product slug used to query endoflife.date.
- <a id="properties/product_found"></a>**`product_found`** _(boolean, required)_: Whether the product was found on endoflife.date.
- <a id="properties/tag"></a>**`tag`** _(string, required)_: Image tag that was analyzed.
- <a id="properties/matched_cycle"></a>**`matched_cycle`** _(object or null, required)_: Release cycle matching the image tag, or null if no match. Cannot contain additional properties.
  - <a id="properties/matched_cycle/properties/cycle"></a>**`cycle`** _(string)_
  - <a id="properties/matched_cycle/properties/release_date"></a>**`release_date`** _(string or null)_
  - <a id="properties/matched_cycle/properties/eol"></a>**`eol`** _(string or boolean)_
  - <a id="properties/matched_cycle/properties/latest"></a>**`latest`** _(string or null)_
  - <a id="properties/matched_cycle/properties/latest_release_date"></a>**`latest_release_date`** _(string or null)_
  - <a id="properties/matched_cycle/properties/lts"></a>**`lts`** _(boolean)_
- <a id="properties/is_eol"></a>**`is_eol`** _(boolean or null, required)_: Whether the matched cycle has reached end-of-life. Null if no match.
- <a id="properties/active_cycles_count"></a>**`active_cycles_count`** _(integer or null, required)_: Number of currently supported release cycles. Minimum: `0`.
- <a id="properties/eol_cycles_count"></a>**`eol_cycles_count`** _(integer or null, required)_: Number of end-of-life release cycles. Minimum: `0`.
