#!/usr/bin/env bash
#
# Phoenix 2.0 Apex Edition — Diagram Export Script
# Export Mermaid diagrams to SVG from Markdown files
# v2.0.0 — Triadic Knot Release
#

set -e
set -o pipefail

# ═══════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════

INPUT_DIR="${1:-Atlases}"
OUTPUT_DIR="${2:-build/svg}"
TEMP_DIR="/tmp/phoenix-mermaid-$$"
LOG_FILE="$OUTPUT_DIR/export.log"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
SCANNED=0
PROCESSED=0
FAILED=0

# ═══════════════════════════════════════════════════════════
# Functions
# ═══════════════════════════════════════════════════════════

log() {
    local timestamp=$(date '+%H:%M:%S')
    echo -e "${BLUE}[${timestamp}]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✓${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠️${NC}  $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}✗${NC} $1" | tee -a "$LOG_FILE"
}

check_dependencies() {
    log "Checking dependencies..."
    
    if command -v mmdc >/dev/null 2>&1; then
        local version=$(mmdc --version 2>/dev/null || echo "unknown")
        success "mmdc found: $version"
        return 0
    else
        warning "mmdc not found"
        echo ""
        echo "Mermaid CLI (mmdc) is required for diagram export."
        echo ""
        echo "Installation options:"
        echo "  npm install -g @mermaid-js/mermaid-cli"
        echo ""
        echo "Alternative (Docker):"
        echo "  docker run --rm -v \$(pwd):/data minlag/mermaid-cli -i input.mmd -o output.svg"
        echo ""
        return 1
    fi
}

extract_mermaid_blocks() {
    local md_file="$1"
    local output_dir="$2"
    local base_name=$(basename "$md_file" .md)
    local count=0
    
    # Extract all ```mermaid blocks from the markdown file
    awk '
        /^```mermaid/ { in_block=1; block=""; next }
        in_block && /^```/ { 
            in_block=0
            count++
            filename=sprintf("%s_%02d.mmd", base_name, count)
            print block > (output_dir "/" filename)
            next
        }
        in_block { block = block $0 "\n" }
    ' base_name="$base_name" output_dir="$output_dir" "$md_file"
    
    # Count extracted diagrams
    count=$(find "$output_dir" -name "${base_name}_*.mmd" 2>/dev/null | wc -l)
    echo "$count"
}

process_standalone_mermaid() {
    local mmd_file="$1"
    local output_svg="$2"
    
    if mmdc -i "$mmd_file" -o "$output_svg" -b transparent >> "$LOG_FILE" 2>&1; then
        success "Generated: $(basename "$output_svg")"
        return 0
    else
        error "Failed to generate: $(basename "$output_svg")"
        return 1
    fi
}

process_markdown_file() {
    local md_file="$1"
    
    log "Scanning: $md_file"
    SCANNED=$((SCANNED + 1))
    
    # Extract mermaid blocks to temp directory
    local extracted_count=$(extract_mermaid_blocks "$md_file" "$TEMP_DIR")
    
    if [ "$extracted_count" -eq 0 ]; then
        log "  No diagrams found"
        return 0
    fi
    
    success "Extracted $extracted_count diagram(s)"
    
    # Process each extracted diagram
    local base_name=$(basename "$md_file" .md)
    for mmd_file in "$TEMP_DIR/${base_name}"_*.mmd; do
        if [ -f "$mmd_file" ]; then
            local diagram_name=$(basename "$mmd_file" .mmd)
            local output_svg="$OUTPUT_DIR/${diagram_name}.svg"
            
            log "Rendering: $(basename "$mmd_file")"
            
            if process_standalone_mermaid "$mmd_file" "$output_svg"; then
                PROCESSED=$((PROCESSED + 1))
            else
                FAILED=$((FAILED + 1))
            fi
        fi
    done
}

cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

# ═══════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════

trap cleanup EXIT

# Print header
echo "═══════════════════════════════════════════════════════════"
echo "  Phoenix 2.0 Apex Edition — Diagram Export"
echo "  Triadic Knot Release (v2.0.0)"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Create output directory and temp directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

# Initialize log file
echo "Phoenix 2.0 Diagram Export — $(date)" > "$LOG_FILE"
echo "═══════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Check dependencies
if ! check_dependencies; then
    error "Required dependencies not found"
    exit 1
fi

log "Input directory:  $INPUT_DIR"
log "Output directory: $OUTPUT_DIR"
echo ""

# Check if input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    error "Input directory not found: $INPUT_DIR"
    exit 1
fi

# Process all markdown files
find "$INPUT_DIR" -name "*.md" -type f | while read -r md_file; do
    process_markdown_file "$md_file"
done

# Process standalone .mmd files
find "$INPUT_DIR" -name "*.mmd" -type f | while read -r mmd_file; do
    log "Processing standalone: $mmd_file"
    SCANNED=$((SCANNED + 1))
    
    base_name=$(basename "$mmd_file" .mmd)
    output_svg="$OUTPUT_DIR/${base_name}.svg"
    
    if process_standalone_mermaid "$mmd_file" "$output_svg"; then
        PROCESSED=$((PROCESSED + 1))
    else
        FAILED=$((FAILED + 1))
    fi
done

# Print summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Export Summary"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Total files scanned:    $SCANNED"
echo "  Successfully processed: $PROCESSED"
echo "  Failed:                 $FAILED"
echo "  Output directory:       $OUTPUT_DIR"
echo ""

if [ "$FAILED" -eq 0 ]; then
    success "All diagrams exported successfully! 🔥"
    exit 0
else
    error "Some diagrams failed to export. Check $LOG_FILE for details."
    exit 1
fi
