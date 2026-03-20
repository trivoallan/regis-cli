# Scorecard Analyzer Report

_Report containing OpenSSF Scorecard security assessment for the image source repository._

## Properties

- <a id="properties/analyzer"></a>**`analyzer`** _(string, required)_: Must be: `"scorecarddev"`.
- <a id="properties/repository"></a>**`repository`** _(string, required)_: Docker image repository path.
- <a id="properties/source_repo"></a>**`source_repo`** _(string or null, required)_: Resolved source code repository URL, or null if not found.
- <a id="properties/scorecard_available"></a>**`scorecard_available`** _(boolean, required)_: Whether OpenSSF Scorecard data was successfully retrieved.
- <a id="properties/score"></a>**`score`** _(number or null, required)_: Overall Scorecard score (0-10), or null if unavailable.
- <a id="properties/checks"></a>**`checks`** _(array, required)_: Individual Scorecard check results.
  - <a id="properties/checks/items"></a>**Items** _(object)_: Cannot contain additional properties.
    - <a id="properties/checks/items/properties/name"></a>**`name`** _(string, required)_: Check name (e.g. Maintained, Code-Review, Vulnerabilities).
    - <a id="properties/checks/items/properties/score"></a>**`score`** _(integer, required)_: Check score (-1 to 10). -1 means not applicable.
    - <a id="properties/checks/items/properties/reason"></a>**`reason`** _(string, required)_: Human-readable explanation of the score.
