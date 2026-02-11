#!/bin/bash
# build-pdf.sh - Build Phoenix 2.0 Codex PDF from Markdown sources
# Usage: build-pdf.sh <build_dir> <output_dir>

set -euo pipefail

BUILD_DIR="${1:-build}"
OUTPUT_DIR="${2:-output}"

echo "📖 Phoenix 2.0 Codex PDF Builder"
echo "================================"

# Check if pandoc is available
if ! command -v pandoc &> /dev/null; then
    echo "⚠️  pandoc is not installed. Attempting to install..."
    # Try to install pandoc
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y pandoc texlive-xetex texlive-latex-extra
    else
        echo "❌ Could not install pandoc automatically"
        echo "Please install pandoc manually: https://pandoc.org/installing.html"
        exit 1
    fi
fi

# Create LaTeX cover page
echo "🎨 Generating Codex cover page..."
cat > "$BUILD_DIR/cover.tex" << 'EOF'
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{patterns,decorations.pathmorphing}

\geometry{margin=1in}
\pagecolor{black}
\color{white}

\begin{document}
\thispagestyle{empty}

\begin{center}
\vspace*{2cm}

% Phoenix Symbol
\begin{tikzpicture}[scale=1.5]
  \draw[line width=2pt, orange!80!red] (0,0) -- (-1.5,-2);
  \draw[line width=2pt, orange!80!red] (0,0) -- (1.5,-2);
  \draw[line width=2pt, orange!80!red] (0,0) -- (0,2.5);
  \draw[line width=1.5pt, yellow!70!orange] (-0.5,1) .. controls (-1,1.5) .. (-0.8,2.2);
  \draw[line width=1.5pt, yellow!70!orange] (0.5,1) .. controls (1,1.5) .. (0.8,2.2);
  \fill[yellow!90!orange] (0,2.5) circle (0.15);
\end{tikzpicture}

\vspace{1.5cm}

{\Huge\textbf{\textsf{PHOENIX 2.0}}}

\vspace{0.5cm}

{\Large\textbf{\textsf{Apex Edition}}}

\vspace{2cm}

{\large\textit{A Self-Contained Symbolic Framework}}

\vspace{0.5cm}

{\large\textit{For Transformation, Recursion, and Emergence}}

\vspace{3cm}

\begin{tikzpicture}
  \draw[line width=1pt, white] (-3,0) -- (3,0);
\end{tikzpicture}

\vspace{0.5cm}

{\large THE CODEX}

\vspace{0.3cm}

{\normalsize Eight Operators · Five Universal Laws · Three Rituals}

\vspace{2cm}

{\small \texttt{⊕ ⊗ ⊛ △ ⊝ ⊞ ⊳ ⊲}}

\end{center}

\end{document}
EOF

# Create LaTeX preamble for main document
echo "📝 Preparing document structure..."
cat > "$BUILD_DIR/preamble.tex" << 'EOF'
---
documentclass: article
geometry: margin=1in
fontsize: 11pt
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes: |
  \usepackage{fancyhdr}
  \usepackage{graphicx}
  \usepackage{xcolor}
  \pagestyle{fancy}
  \fancyhead[L]{Phoenix 2.0 — Apex Edition}
  \fancyhead[R]{\thepage}
  \fancyfoot[C]{The Codex}
---
EOF

# Compile cover page
echo "🔥 Compiling cover page..."
cd "$BUILD_DIR"
if command -v pdflatex &> /dev/null; then
    pdflatex -interaction=nonstopmode cover.tex > /dev/null 2>&1 || echo "⚠️  LaTeX cover page generation failed, continuing without it..."
    cd ..
else
    echo "⚠️  pdflatex not available, skipping cover page generation"
    cd ..
fi

# Combine all markdown files
echo "📚 Combining markdown sources..."
cat > "$BUILD_DIR/combined.md" << 'EOF'
---
title: "Phoenix 2.0 — Apex Edition"
subtitle: "The Complete Codex"
author: "The Phoenix Collective"
date: "2026"
---

\newpage
EOF

# Add main content
cat README.md >> "$BUILD_DIR/combined.md"
echo -e "\n\n\\newpage\n\n# PART I: OPERATORS\n" >> "$BUILD_DIR/combined.md"

for op in operators/*.md; do
    [ -f "$op" ] || continue
    echo -e "\n\\newpage\n" >> "$BUILD_DIR/combined.md"
    cat "$op" >> "$BUILD_DIR/combined.md"
done

echo -e "\n\n\\newpage\n\n# PART II: UNIVERSAL LAWS\n" >> "$BUILD_DIR/combined.md"

for law in laws/*.md; do
    [ -f "$law" ] || continue
    echo -e "\n\\newpage\n" >> "$BUILD_DIR/combined.md"
    cat "$law" >> "$BUILD_DIR/combined.md"
done

echo -e "\n\n\\newpage\n\n# PART III: RITUALS\n" >> "$BUILD_DIR/combined.md"

for ritual in rituals/*.md; do
    [ -f "$ritual" ] || continue
    echo -e "\n\\newpage\n" >> "$BUILD_DIR/combined.md"
    cat "$ritual" >> "$BUILD_DIR/combined.md"
done

# Generate PDF using pandoc
echo "📄 Generating PDF with pandoc..."
if pandoc "$BUILD_DIR/combined.md" \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=2 \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    -o "$OUTPUT_DIR/Phoenix-2.0-Codex.pdf" 2>&1; then
    echo "✓ PDF successfully generated"
else
    echo "⚠️  Pandoc PDF generation failed, trying alternative method..."
    # Fallback: create a simpler PDF without LaTeX
    pandoc "$BUILD_DIR/combined.md" \
        --toc \
        -o "$OUTPUT_DIR/Phoenix-2.0-Codex.pdf" || {
        echo "❌ PDF generation failed"
        echo "Creating a basic HTML version instead..."
        pandoc "$BUILD_DIR/combined.md" \
            --toc \
            --standalone \
            -o "$OUTPUT_DIR/Phoenix-2.0-Codex.html"
        echo "✓ HTML version created at $OUTPUT_DIR/Phoenix-2.0-Codex.html"
    }
fi

echo ""
echo "✨ Build complete!"
echo "Output: $OUTPUT_DIR/Phoenix-2.0-Codex.pdf"
