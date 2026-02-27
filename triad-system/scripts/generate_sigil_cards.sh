#!/bin/bash
# generate_sigil_cards.sh
# Generates SVG sigil cards for the Triad System operators

set -e

# Configuration
OUTPUT_DIR="output/sigils"
TEMPLATE_WIDTH=400
TEMPLATE_HEIGHT=600

# Colors (Phoenix 2.0 palette)
COLOR_GENESIS="#FF6B35"
COLOR_HARMONIC="#F7931E"
COLOR_RECURSIVE="#FDC830"
COLOR_APEX="#C84B31"
COLOR_VOID="#2D4654"
COLOR_MIRROR="#5C94BD"
COLOR_CONVERGENCE="#8B5FBF"
COLOR_DIVERGENCE="#D64161"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Generating Triad System sigil cards..."

# Function to generate a sigil card
generate_sigil() {
    local name=$1
    local symbol=$2
    local color=$3
    local output_file="$OUTPUT_DIR/${name,,}.svg"
    
    cat > "$output_file" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<svg width="$TEMPLATE_WIDTH" height="$TEMPLATE_HEIGHT" 
     xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink">
  
  <!-- Background -->
  <rect width="$TEMPLATE_WIDTH" height="$TEMPLATE_HEIGHT" fill="#1a1a1a" rx="10"/>
  
  <!-- Border -->
  <rect x="10" y="10" width="380" height="580" 
        fill="none" stroke="$color" stroke-width="2" rx="5"/>
  
  <!-- Title -->
  <text x="200" y="50" 
        font-family="Arial, sans-serif" 
        font-size="24" 
        font-weight="bold"
        fill="$color" 
        text-anchor="middle">$name</text>
  
  <!-- Symbol -->
  <text x="200" y="320" 
        font-family="Arial, sans-serif" 
        font-size="120" 
        fill="$color" 
        text-anchor="middle">$symbol</text>
  
  <!-- Footer line -->
  <line x1="50" y1="500" x2="350" y2="500" 
        stroke="$color" stroke-width="1"/>
  
  <!-- Label -->
  <text x="200" y="550" 
        font-family="Arial, sans-serif" 
        font-size="14" 
        fill="#cccccc" 
        text-anchor="middle">Phoenix 2.0 Triad System</text>
  
</svg>
EOF
    
    echo "  Generated: $output_file"
}

# Generate sigil cards for each operator
generate_sigil "Genesis" "⊕" "$COLOR_GENESIS"
generate_sigil "Harmonic" "⊗" "$COLOR_HARMONIC"
generate_sigil "Recursive" "⊛" "$COLOR_RECURSIVE"
generate_sigil "Apex" "△" "$COLOR_APEX"
generate_sigil "Void" "⊝" "$COLOR_VOID"
generate_sigil "Mirror" "⊞" "$COLOR_MIRROR"
generate_sigil "Convergence" "⊳" "$COLOR_CONVERGENCE"
generate_sigil "Divergence" "⊲" "$COLOR_DIVERGENCE"

echo ""
echo "✓ Generated 8 sigil cards in $OUTPUT_DIR/"
echo ""
