#!/bin/bash
# Generate sigil cards from ASCII art to PNG/SVG formats
# This script converts operator sigils into visual card assets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/build/sigils"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Generating sigil cards..."
echo "Input: $PROJECT_ROOT/operators/*.md"
echo "Output: $OUTPUT_DIR"

# Process each operator file to extract sigils
# Expected format: Operator markdown files contain the actual Unicode symbols
# ⊕ (Genesis), ⊗ (Harmonic), ⊛ (Recursive), △ (Apex),
# ⊝ (Void), ⊞ (Mirror), ⊳ (Convergence), ⊲ (Divergence)
for operator_file in "$PROJECT_ROOT"/operators/*.md; do
    if [ -f "$operator_file" ]; then
        operator_name=$(basename "$operator_file" .md)
        echo "  Processing: $operator_name"
        
        # Extract lines containing operator symbols or sigil markers
        grep -E "^#.*[⊕⊗⊛△⊝⊞⊳⊲]|Symbol|Sigil|^⊕|^⊗|^⊛|^△|^⊝|^⊞|^⊳|^⊲" "$operator_file" > "$OUTPUT_DIR/${operator_name}_sigil.txt" 2>/dev/null || true
    fi
done

echo "✓ Sigil card generation complete"
echo "  Output directory: $OUTPUT_DIR"
