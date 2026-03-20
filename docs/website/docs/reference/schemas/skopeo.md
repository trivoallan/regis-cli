# Skopeo Analyzer Report

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"skopeo"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_
- <a id="properties/tag"></a>**`tag`** _(string, required)_
- <a id="properties/inspect"></a>**`inspect`** _(object)_: Raw output from primary skopeo inspect.
- <a id="properties/platforms"></a>**`platforms`** _(array, required)_: List of platform variants available for this tag.
  - <a id="properties/platforms/items"></a>**Items** _(object)_
    - <a id="properties/platforms/items/properties/architecture"></a>**`architecture`** _(string, required)_
    - <a id="properties/platforms/items/properties/os"></a>**`os`** _(string, required)_
    - <a id="properties/platforms/items/properties/variant"></a>**`variant`** _(string or null)_
    - <a id="properties/platforms/items/properties/digest"></a>**`digest`** _(string)_
    - <a id="properties/platforms/items/properties/created"></a>**`created`** _(string or null)_
    - <a id="properties/platforms/items/properties/labels"></a>**`labels`** _(object)_: Can contain additional properties.
      - <a id="properties/platforms/items/properties/labels/additionalProperties"></a>**Additional properties** _(string)_
    - <a id="properties/platforms/items/properties/layers_count"></a>**`layers_count`** _(integer)_: Minimum: `0`.
    - <a id="properties/platforms/items/properties/user"></a>**`user`** _(string or null)_
- <a id="properties/tags"></a>**`tags`** _(array)_: List of tags associated with the repository.
  - <a id="properties/tags/items"></a>**Items** _(string)_
