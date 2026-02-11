#!/bin/bash
# Export Mermaid diagrams to SVG format
# Phoenix 2.0 — Apex Edition

set -e

OUTPUT_DIR="build/svg"
DOCS_DIR="docs"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Exporting Mermaid diagrams to SVG..."

# Check if mmdc (mermaid-cli) is installed
if ! command -v mmdc >/dev/null 2>&1; then
    echo "⚠ Warning: mermaid-cli (mmdc) not found"
    echo "  Install: npm install -g @mermaid-js/mermaid-cli"
    echo "  Skipping SVG export."
    exit 0
fi

# Extract and export diagrams from docs/diagrams.md
DIAGRAM_FILE="$DOCS_DIR/diagrams.md"

if [ ! -f "$DIAGRAM_FILE" ]; then
    echo "Error: $DIAGRAM_FILE not found"
    exit 1
fi

# Function to extract Mermaid code blocks and convert to SVG
extract_and_convert() {
    local input_file="$1"
    local output_prefix="$2"
    local counter=1
    local in_mermaid=false
    local temp_mmd="/tmp/temp_diagram_$$.mmd"
    
    while IFS= read -r line; do
        if [[ "$line" == '```mermaid' ]]; then
            in_mermaid=true
            > "$temp_mmd"  # Clear temp file
        elif [[ "$line" == '```' ]] && [ "$in_mermaid" = true ]; then
            in_mermaid=false
            # Convert to SVG
            local output_file="$OUTPUT_DIR/${output_prefix}_${counter}.svg"
            if mmdc -i "$temp_mmd" -o "$output_file" -b transparent 2>/dev/null; then
                echo "  ✓ Exported: ${output_prefix}_${counter}.svg"
                ((counter++))
            fi
        elif [ "$in_mermaid" = true ]; then
            echo "$line" >> "$temp_mmd"
        fi
    done < "$input_file"
    
    rm -f "$temp_mmd"
    return $((counter - 1))
}

# Export diagrams from main diagram file
echo "Processing $DIAGRAM_FILE..."
count=$(extract_and_convert "$DIAGRAM_FILE" "diagram")

# Also check for diagrams in other docs
for doc in "$DOCS_DIR"/*.md; do
    if [ "$doc" != "$DIAGRAM_FILE" ] && [ -f "$doc" ]; then
        basename=$(basename "$doc" .md)
        echo "Processing $doc..."
        extract_and_convert "$doc" "$basename" > /dev/null
    fi
done

# Create index file
cat > "$OUTPUT_DIR/README.md" << 'EOF'
# SVG Diagrams

This directory contains SVG exports of all Mermaid diagrams from the Codex documentation.

## Files

Generated diagram files follow the naming pattern:
- `diagram_N.svg` — Diagrams from docs/diagrams.md
- `{filename}_N.svg` — Diagrams from other documentation files

## Usage

### View in Browser
Open any `.svg` file in a web browser:
```bash
firefox build/svg/diagram_1.svg
```

### Embed in HTML
```html
<img src="build/svg/diagram_1.svg" alt="System Stack">
```

### Embed in Markdown
```markdown
![System Stack](build/svg/diagram_1.svg)
```

### Convert to PNG
Using ImageMagick:
```bash
convert build/svg/diagram_1.svg build/svg/diagram_1.png
```

## Regeneration

To regenerate all SVG files:
```bash
make svg
# or
bash scripts/export-svg.sh
```

## Requirements

- `mmdc` (mermaid-cli) — Install with: `npm install -g @mermaid-js/mermaid-cli`
- Chromium or Chrome (required by mermaid-cli for rendering)
EOF

echo ""
echo "✓ SVG export complete"
echo "Output directory: $OUTPUT_DIR"
