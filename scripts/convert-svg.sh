#!/bin/bash
# convert-svg.sh - Convert PDF pages to SVG format
# Usage: convert-svg.sh <pdf_file> <output_dir>

set -euo pipefail

PDF_FILE="${1:-output/Phoenix-2.0-Codex.pdf}"
OUTPUT_DIR="${2:-output}"

echo "🎨 Phoenix 2.0 PDF to SVG Converter"
echo "===================================="

# Check if PDF file exists
if [ ! -f "$PDF_FILE" ]; then
    echo "❌ PDF file not found: $PDF_FILE"
    exit 1
fi

# Check for conversion tools
HAS_PDFTOCAIRO=false
HAS_INKSCAPE=false
HAS_CONVERT=false

if command -v pdftocairo &> /dev/null; then
    HAS_PDFTOCAIRO=true
    echo "✓ Found pdftocairo"
fi

if command -v inkscape &> /dev/null; then
    HAS_INKSCAPE=true
    echo "✓ Found inkscape"
fi

if command -v convert &> /dev/null; then
    HAS_CONVERT=true
    echo "✓ Found ImageMagick convert"
fi

# Try different conversion methods
if $HAS_PDFTOCAIRO; then
    echo "📄 Converting PDF to SVG using pdftocairo..."
    pdftocairo -svg "$PDF_FILE" "$OUTPUT_DIR/Phoenix-2.0-Codex.svg" && {
        echo "✓ SVG generated successfully"
        exit 0
    }
elif $HAS_INKSCAPE; then
    echo "📄 Converting PDF to SVG using Inkscape..."
    inkscape --pdf-poppler --export-type=svg "$PDF_FILE" -o "$OUTPUT_DIR/Phoenix-2.0-Codex.svg" && {
        echo "✓ SVG generated successfully"
        exit 0
    }
elif $HAS_CONVERT; then
    echo "📄 Converting PDF to SVG using ImageMagick..."
    convert -density 300 "$PDF_FILE" "$OUTPUT_DIR/Phoenix-2.0-Codex.svg" && {
        echo "✓ SVG generated successfully"
        exit 0
    }
else
    echo "⚠️  No PDF to SVG converter found"
    echo "Please install one of the following:"
    echo "  - pdftocairo (poppler-utils)"
    echo "  - inkscape"
    echo "  - ImageMagick"
    echo ""
    echo "Attempting to install poppler-utils..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y poppler-utils && {
            echo "✓ poppler-utils installed"
            pdftocairo -svg "$PDF_FILE" "$OUTPUT_DIR/Phoenix-2.0-Codex.svg"
            echo "✓ SVG generated successfully"
            exit 0
        }
    fi
    echo "❌ Could not convert PDF to SVG"
    exit 1
fi

echo ""
echo "✨ Conversion complete!"
echo "Output: $OUTPUT_DIR/Phoenix-2.0-Codex.svg"
