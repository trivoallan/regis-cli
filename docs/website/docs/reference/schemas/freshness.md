# Freshness Analyzer Report

_Image age and delta versus latest tag._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"freshness"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/tag_created"></a>**`tag_created`** _(string or null, required)_
- <a id="properties/latest_created"></a>**`latest_created`** _(string or null, required)_
- <a id="properties/age_days"></a>**`age_days`** _(integer or null, required)_: Minimum: `0`.
- <a id="properties/behind_latest_days"></a>**`behind_latest_days`** _(integer or null, required)_: Minimum: `0`.
- <a id="properties/is_latest"></a>**`is_latest`** _(boolean, required)_
