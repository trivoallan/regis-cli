#!/bin/bash

# Update example links in markdown files to point to correct versioned paths
# Usage: scripts/update_example_links.sh [version]

set -e

VERSION="${1:-main}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Determine the correct base URL for example links
if [ "$VERSION" = "main" ]; then
    EXAMPLE_BASE_URL="/docs/examples/playbooks/default"
else
    EXAMPLE_BASE_URL="/docs/version-${VERSION}/examples/playbooks/default"
fi

echo "Updating example links for version: $VERSION"
echo "Example base URL: $EXAMPLE_BASE_URL"
echo ""

# Find all markdown files in the appropriate docs directory
if [ "$VERSION" = "main" ]; then
    DOCS_PATH="$PROJECT_ROOT/docs/website/docs"
else
    DOCS_PATH="$PROJECT_ROOT/docs/website/versioned_docs/version-${VERSION}"
fi

# Update links in example files
find "$DOCS_PATH/reference/playbooks/default/examples" -name "*.md" 2>/dev/null | while read -r FILE; do
    EXAMPLE_NAME=$(basename "$FILE" .md)
    echo "Updating $FILE..."
    
    # Replace old pathname:/// links with correct paths
    sed -i.bak \
        "s|pathname:///regis/examples/playbooks/default/${EXAMPLE_NAME}/|${EXAMPLE_BASE_URL}/${EXAMPLE_NAME}/|g" \
        "$FILE"
    
    # Clean up backup
    rm -f "${FILE}.bak"
done

# Update main index/intro files
find "$DOCS_PATH" -maxdepth 1 -name "*.md*" 2>/dev/null | while read -r FILE; do
    if grep -q "pathname:///.*examples/playbooks" "$FILE"; then
        echo "Updating $FILE..."
        sed -i.bak \
            "s|pathname:///regis/examples/playbooks|${EXAMPLE_BASE_URL}|g" \
            "$FILE"
        rm -f "${FILE}.bak"
    fi
done

echo "✓ Example links updated successfully"
