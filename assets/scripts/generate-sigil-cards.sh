#!/bin/bash
# Generate Sigil Cards for Phoenix 2.0 Apex Edition
# Creates printable PDF cards for all operators and laws

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$(dirname "$SCRIPT_DIR")"
LATEX_DIR="$ASSETS_DIR/latex"
BUILD_DIR="$LATEX_DIR/build"
CARDS_DIR="$BUILD_DIR/cards"

echo "Phoenix 2.0 Apex Edition - Sigil Card Generator"
echo "================================================"
echo ""

# Check for XeLaTeX
if ! command -v xelatex &> /dev/null; then
    echo "ERROR: xelatex not found"
    echo "Install with: sudo apt-get install texlive-xetex"
    exit 1
fi

# Create output directory
mkdir -p "$CARDS_DIR"

# Card data: Name|Symbol|Subtitle|Sigil
declare -a CARDS=(
    "Genesis Operator|⊕|Initial creation from void|    ⊕\n   ╱│╲\n  ∅ ⊕ ∃"
    "Harmonic Operator|⊗|Resonance binding|  ⊗═══⊗\n ╱│╲ ╱│╲\n⊗═⊗═⊗═⊗═⊗"
    "Recursive Operator|⊛|Self-reference pattern|    ⊛\n   ╱│╲\n  ⊛ ⊛ ⊛"
    "Apex Operator|△|Triad formation|      △\n     ╱ ╲\n    ╱   ╲\n   ●─────●"
    "Void Operator|⊝|Nullification|    ⊝\n   ╱│╲\n  ∃ ⊝ ∅"
    "Mirror Operator|⊞|Reflection|  ●═══⊞═══●\n  ║   ║   ║\n  ⊞═══⊞═══⊞"
    "Convergence Operator|⊳|Unification|  ● → ⊳\n  ●  ↗ ↘  ●\n  ● →  ⊳  → ●"
    "Divergence Operator|⊲|Separation|       ⊲ → ●\n     ↗   ↘\n  ● →  ⊲  → ●"
)

# Function to generate a single card
generate_card() {
    local name="$1"
    local symbol="$2"
    local subtitle="$3"
    local sigil="$4"
    local output="$5"
    
    echo "Generating: $name..."
    
    # Create temporary LaTeX file
    local temp_tex="$BUILD_DIR/temp_card.tex"
    
    cat > "$temp_tex" <<EOF
% Auto-generated sigil card
\documentclass[10pt,landscape]{article}

\usepackage[
  paperwidth=4in,
  paperheight=3in,
  margin=0.25in
]{geometry}

\usepackage{fontspec}
\setmainfont{EB Garamond}
\setmonofont{Fira Code}

\usepackage{xcolor}
\definecolor{cardcolor}{RGB}{184,134,11}

\pagestyle{empty}

\usepackage{tcolorbox}

\begin{document}

\begin{tcolorbox}[
  colback=white,
  colframe=cardcolor,
  width=\textwidth,
  height=2.5in,
  boxrule=2pt,
  arc=3pt,
  valign=center
]
  {\centering\Large\bfseries $symbol $name\par}
  \vspace{4pt}
  {\centering\small\itshape $subtitle\par}
  \vspace{8pt}
  {\centering\ttfamily\normalsize
  \begin{tabular}{c}
$(echo -e "$sigil")
  \end{tabular}
  \par}
\end{tcolorbox}

\end{document}
EOF
    
    # Compile LaTeX
    cd "$BUILD_DIR"
    xelatex -interaction=nonstopmode -halt-on-error "$temp_tex" > /dev/null 2>&1
    
    # Move output
    if [ -f "temp_card.pdf" ]; then
        mv "temp_card.pdf" "$output"
        echo "  Created: $output"
    else
        echo "  ERROR: Failed to generate $output"
        return 1
    fi
    
    # Cleanup
    rm -f temp_card.{aux,log,tex}
}

# Generate all cards
echo "Generating cards..."
echo ""

for card_data in "${CARDS[@]}"; do
    IFS='|' read -r name symbol subtitle sigil <<< "$card_data"
    
    # Create filename
    filename=$(echo "$name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-').pdf
    output_path="$CARDS_DIR/$filename"
    
    generate_card "$name" "$symbol" "$subtitle" "$sigil" "$output_path"
done

echo ""
echo "Complete! Cards generated in:"
echo "  $CARDS_DIR"
echo ""
echo "Card count: $(ls -1 "$CARDS_DIR"/*.pdf 2>/dev/null | wc -l)"
echo ""
echo "To print: Open PDFs and print 4x3 inch cards"
echo "To combine: Use pdftk or similar to merge all cards"
