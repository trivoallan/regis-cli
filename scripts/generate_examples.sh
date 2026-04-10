#!/bin/bash

# Generate playbook examples for a specific version
# Usage: scripts/generate_examples.sh [version]
#
# Examples:
#   scripts/generate_examples.sh         # Generate for main-dev
#   scripts/generate_examples.sh v0.28.1 # Generate for version v0.28.1

set -e

VERSION="${1:-main}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Determine output directory based on version
if [ "$VERSION" = "main" ]; then
    EXAMPLES_DIR="$PROJECT_ROOT/docs/website/static/examples/playbooks/default"
    BASE_URL="/regis/examples/playbooks/default"
    DOC_BASE_URL="/docs/examples/playbooks/default"
else
    EXAMPLES_DIR="$PROJECT_ROOT/docs/website/versioned_docs/version-${VERSION}/static/examples/playbooks/default"
    BASE_URL="/regis/docs/version-${VERSION}/examples/playbooks/default"
    DOC_BASE_URL="/docs/version-${VERSION}/examples/playbooks/default"
fi

echo "Generating examples for version: $VERSION"
echo "Output directory: $EXAMPLES_DIR"
echo "Base URL: $BASE_URL"
echo ""

# Create output directory
mkdir -p "$EXAMPLES_DIR"

# Define examples to generate
declare -a EXAMPLES=(
    "alpine:latest"
)

# Generate each example
for EXAMPLE in "${EXAMPLES[@]}"; do
    EXAMPLE_NAME=$(echo "$EXAMPLE" | cut -d: -f1)
    EXAMPLE_DIR="$EXAMPLES_DIR/$EXAMPLE_NAME"

    echo "Generating example: $EXAMPLE"
    echo "Output: $EXAMPLE_DIR"

    cd "$PROJECT_ROOT"

    # Generate the example
    pipenv run regis analyze "$EXAMPLE" \
        --evaluate \
        --site \
        --base-url "$BASE_URL/$EXAMPLE_NAME/" \
        --output-dir "$EXAMPLE_DIR" || {
        echo "Failed to generate example: $EXAMPLE"
        exit 1
    }

    echo "✓ Generated $EXAMPLE_NAME successfully"
    echo ""
done

echo "✓ All examples generated successfully for version: $VERSION"
