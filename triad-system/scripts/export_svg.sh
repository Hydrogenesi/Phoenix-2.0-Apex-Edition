#!/bin/bash
# export_svg.sh
# Exports LaTeX diagrams and figures to SVG format

set -e

# Configuration
OUTPUT_DIR="output/svg"
CODEX_DIR="codex"
BUILD_DIR="build"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Exporting diagrams to SVG format..."

# Check if LaTeX output exists
if [ ! -d "$BUILD_DIR" ]; then
    echo "Warning: Build directory not found. Run 'make codex' first."
    exit 1
fi

# Function to export PDF page to SVG
export_pdf_to_svg() {
    local pdf_file=$1
    local page_num=$2
    local output_name=$3
    local output_file="$OUTPUT_DIR/$output_name.svg"
    
    # Use pdf2svg if available, otherwise fall back to Inkscape
    if command -v pdf2svg &> /dev/null; then
        pdf2svg "$pdf_file" "$output_file" "$page_num"
        echo "  Exported: $output_file (using pdf2svg)"
    elif command -v inkscape &> /dev/null; then
        inkscape --pdf-page="$page_num" --export-type=svg \
                 --export-filename="$output_file" "$pdf_file"
        echo "  Exported: $output_file (using inkscape)"
    else
        echo "  Warning: Neither pdf2svg nor inkscape found. Skipping SVG export."
        echo "  Install pdf2svg or inkscape to enable diagram export."
        return 1
    fi
}

# Check for codex PDF
CODEX_PDF="$BUILD_DIR/codex.pdf"
if [ -f "$CODEX_PDF" ]; then
    echo "Found codex PDF, attempting to extract diagrams..."
    
    # Export key diagrams (example page numbers - adjust as needed)
    # export_pdf_to_svg "$CODEX_PDF" 5 "triad-axis-diagram"
    # export_pdf_to_svg "$CODEX_PDF" 8 "topology-diagram"
    # export_pdf_to_svg "$CODEX_PDF" 12 "kernel-architecture"
    
    echo "Note: Diagram extraction requires page numbers to be configured."
    echo "Edit this script to specify which pages contain diagrams."
else
    echo "Codex PDF not found at $CODEX_PDF"
    echo "Run 'make codex' first to generate the PDF."
fi

# Alternative: Export standalone TikZ diagrams if they exist
if [ -d "$CODEX_DIR/diagrams" ]; then
    echo "Searching for standalone diagram files..."
    for tex_file in "$CODEX_DIR/diagrams"/*.tex; do
        if [ -f "$tex_file" ]; then
            diagram_name=$(basename "$tex_file" .tex)
            echo "  Processing: $diagram_name"
            
            # Compile to PDF then convert to SVG
            pdflatex -output-directory="$BUILD_DIR" "$tex_file" > /dev/null 2>&1
            if [ -f "$BUILD_DIR/$diagram_name.pdf" ]; then
                export_pdf_to_svg "$BUILD_DIR/$diagram_name.pdf" 1 "$diagram_name"
            fi
        fi
    done
fi

echo ""
echo "✓ SVG export complete. Files available in $OUTPUT_DIR/"
echo ""
