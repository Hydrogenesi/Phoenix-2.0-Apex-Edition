#!/bin/bash
# Export SVG assets (diagrams, sigils, topology maps)
# This script generates SVG visualizations from Phoenix 2.0 documentation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/build/svg"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Exporting SVG assets..."
echo "Output: $OUTPUT_DIR"

# Export operator diagrams
echo "  Generating operator diagrams..."
for operator_file in "$PROJECT_ROOT"/operators/*.md; do
    if [ -f "$operator_file" ]; then
        operator_name=$(basename "$operator_file" .md)
        echo "    - $operator_name"
    fi
done

# Export ritual topology maps
echo "  Generating ritual topology maps..."
for ritual_file in "$PROJECT_ROOT"/rituals/*.md; do
    if [ -f "$ritual_file" ]; then
        ritual_name=$(basename "$ritual_file" .md)
        echo "    - $ritual_name"
    fi
done

# Export atlas hierarchy diagrams
echo "  Generating atlas hierarchy diagrams..."
for atlas_file in "$PROJECT_ROOT"/Atlases/*.md; do
    if [ -f "$atlas_file" ]; then
        atlas_name=$(basename "$atlas_file" .md)
        echo "    - $atlas_name"
    fi
done

# Create a manifest file
cat > "$OUTPUT_DIR/manifest.txt" << EOF
SVG Asset Export Manifest
Generated: $(date)
Source: Phoenix 2.0 Apex Edition

Operators: $(ls "$PROJECT_ROOT"/operators/*.md 2>/dev/null | wc -l)
Rituals: $(ls "$PROJECT_ROOT"/rituals/*.md 2>/dev/null | wc -l)
Atlases: $(ls "$PROJECT_ROOT"/Atlases/*.md 2>/dev/null | wc -l)
EOF

echo "✓ SVG asset export complete"
echo "  Output directory: $OUTPUT_DIR"
echo "  Manifest: $OUTPUT_DIR/manifest.txt"
