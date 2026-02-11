# LaTeX Production System

## Professional Typesetting for Phoenix 2.0 Apex Edition

---

## Overview

This directory contains LaTeX templates and build infrastructure for generating professional ceremonial documents from the Phoenix-Hydrogenesi codex. The system produces:

- **Complete Codex** - Full bound book with all content
- **Individual Law Cards** - Printable reference cards (4x3 inch)
- **Sigil Sheets** - Large-format ASCII art for ceremonial use
- **Chapter Booklets** - Standalone sections for focused study

---

## Directory Structure

```
assets/latex/
├── README.md              (this file)
├── templates/             LaTeX document templates
│   ├── codex-main.tex        Master document
│   ├── law-template.tex      Individual law format
│   ├── sigil-card.tex        Printable card template
│   └── chapter-template.tex  Chapter formatting
├── chapters/              Content organized by chapter
│   ├── seven-laws.tex
│   ├── substrate.tex
│   ├── universal.tex
│   ├── apex.tex
│   ├── triad.tex
│   ├── phoenix.tex
│   ├── hydrogenesi.tex
│   └── sigils.tex
├── appendices/            Back matter
│   ├── glossary.tex
│   └── operators.tex
└── build/                 Build artifacts and Makefile
    └── Makefile
```

---

## Prerequisites

### Required Packages

```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# macOS
brew install --cask mactex

# Or minimal install:
sudo apt-get install texlive-latex-base \
                     texlive-latex-extra \
                     texlive-fonts-recommended \
                     texlive-xetex
```

### Recommended Fonts

The templates use:
- **EB Garamond** - Body text (ceremonial serif)
- **Cinzel** - Headers (decorative capitals)
- **Fira Code** - Monospace (ASCII sigils)

Install via:
```bash
sudo apt-get install fonts-ebgaramond \
                     fonts-cinzel \
                     fonts-firacode
```

---

## Quick Start

### Build Complete Codex

```bash
cd assets/latex/build
make pdf
```

Output: `Phoenix-Codex-v2.0.pdf` (full book)

---

### Generate Sigil Cards

```bash
cd assets/latex/build
make sigil-cards
```

Output: Individual PDF cards in `build/cards/`

---

### Build Single Chapter

```bash
cd assets/latex/build
make chapter CHAPTER=substrate
```

Output: `build/substrate-chapter.pdf`

---

### Clean Build Artifacts

```bash
cd assets/latex/build
make clean
```

---

## Template Documentation

### codex-main.tex

Master document using `book` class:

**Features**:
- Two-sided layout (inner/outer margins)
- Automatic table of contents
- Chapter headers with custom styling
- Professional typography (microtype, spacing)
- Cross-reference system
- Index generation

**Usage**:
```latex
\documentclass[12pt,twoside]{book}
\input{../templates/preamble}

\begin{document}
\frontmatter
  \maketitle
  \tableofcontents
\mainmatter
  \include{../chapters/seven-laws}
  \include{../chapters/substrate}
  % ... more chapters
\backmatter
  \include{../appendices/glossary}
\end{document}
```

---

### law-template.tex

Standalone law documents using `article` class:

**Features**:
- Structured sections (Statement, Expression, Meaning)
- tcolorbox for emphasis
- Mathematical notation support (amsmath)
- ASCII sigil preservation (verbatim, listings)

**Usage**:
```latex
\documentclass[11pt]{article}
\input{../templates/law-preamble}

\begin{document}
\lawtitle{Law of Recursive Identity}
\lawsubtitle{Universal Law I}

\lawstatement{
Every entity contains the pattern of its own generation.
}

\lawexpression{
$\forall x: x = \recurse(x_0)$
}

\lawmeaning{
Identity is not static but emerges through self-referential...
}

\lawsigil{
    ⊛
   ╱│╲
  ⊛ ⊛ ⊛
}
\end{document}
```

---

### sigil-card.tex

Printable reference cards (4×3 inch landscape):

**Features**:
- Compact layout optimized for printing
- Large monospace sigil display
- Essential metadata (law name, meaning)
- Border for cutting guides

**Usage**:
```latex
\documentclass[landscape]{article}
\usepackage[paperwidth=4in,paperheight=3in]{geometry}

\sigilcard{
  {⊕ Genesis Operator}
  {Initial creation from void}
  {
    ⊕
   ╱│╲
  ∅ ⊕ ∃
  }
}
```

---

### chapter-template.tex

Consistent chapter formatting:

**Features**:
- Standard heading hierarchy
- Cross-reference support
- Mermaid diagram notes (for manual conversion)
- Code listing environments
- Ceremonial section markers

---

## Build System

### Makefile Targets

```makefile
# Primary targets
pdf:           Build complete codex
sigil-cards:   Generate all operator/law cards
chapter:       Build single chapter (requires CHAPTER=name)
clean:         Remove build artifacts
distclean:     Remove all generated files

# Advanced targets
draft:         Quick draft build (no index)
final:         Production build (3-pass with index)
cards-sheet:   All cards on one sheet (for printing)
```

### Build Variables

```makefile
# Override in command line
LATEX = xelatex              # or pdflatex
CHAPTERS = seven-laws substrate universal apex
OUTPUT_DIR = build
CARD_SIZE = 4x3              # inches
```

### Example Commands

```bash
# Draft build (faster)
make draft

# Production with custom output
make final OUTPUT_DIR=dist

# Build specific chapters
make chapter CHAPTER=substrate
make chapter CHAPTER=apex

# Generate card sheet
make cards-sheet
```

---

## Typography Guidelines

### Font Usage

| Context | Font | Size | Purpose |
|---------|------|------|---------|
| Body | EB Garamond | 12pt | Ceremonial readability |
| Headers | Cinzel | 18-24pt | Decorative emphasis |
| Code/Sigils | Fira Code | 10pt | Monospace alignment |
| Captions | EB Garamond | 10pt | Figure labels |

### Spacing

- Line spacing: 1.2 (slight increase for readability)
- Paragraph spacing: 6pt
- Chapter starts: New page (right side in two-sided)
- Section spacing: 12pt above, 6pt below

### Special Environments

```latex
\begin{lawbox}
  Emphasized law content
\end{lawbox}

\begin{sigilenv}
    ⊛
   ╱│╲
  ⊛ ⊛ ⊛
\end{sigilenv}

\begin{ritualsteps}
  1. Preparation
  2. Execution
  3. Integration
\end{ritualsteps}
```

---

## Customization

### Colors

Default ceremonial palette (defined in preamble):

```latex
\definecolor{phoenixred}{RGB}{180,0,0}
\definecolor{hydrogenesiblue}{RGB}{0,60,120}
\definecolor{apexgold}{RGB}{184,134,11}
\definecolor{substratepurple}{RGB}{75,0,130}
```

Override in custom preamble:
```latex
\input{../templates/preamble}
\definecolor{phoenixred}{RGB}{255,0,0}  % Brighter
```

### Page Layout

Adjust margins in preamble:
```latex
\usepackage[
  inner=1.5in,   % Binding side
  outer=1in,     % Outer edge
  top=1in,
  bottom=1.2in
]{geometry}
```

### Header/Footer

Customize running heads:
```latex
\fancyhead[LE,RO]{\thepage}
\fancyhead[LO]{\rightmark}  % Section
\fancyhead[RE]{\leftmark}   % Chapter
```

---

## ASCII Art Preservation

Critical for sigil rendering:

### Requirements

1. **Monospace font**: Use `\ttfamily` or `\texttt{}`
2. **Verbatim environment**: Preserve spacing exactly
3. **Unicode support**: XeLaTeX or LuaLaTeX (not pdflatex)
4. **Font with glyphs**: Fira Code or DejaVu Sans Mono

### Example

```latex
\begin{verbatim}
      △
     ╱ ╲
    ╱   ╲
   ●─────●
\end{verbatim}
```

Or inline: `\verb|⊕ ⊗ ⊛|`

---

## Troubleshooting

### Issue: Missing fonts

**Symptom**: PDF has wrong fonts or missing characters

**Solution**:
```bash
# Rebuild font cache
sudo fc-cache -fv

# Verify font available
fc-list | grep -i garamond
```

---

### Issue: Broken sigils

**Symptom**: ASCII art misaligned or missing glyphs

**Solution**:
- Use XeLaTeX instead of pdflatex
- Install fonts with box-drawing characters
- Check `\usepackage{fontspec}` in preamble

---

### Issue: Build fails

**Symptom**: LaTeX errors during compilation

**Solution**:
```bash
# Check log file
cat build/*.log | grep -i error

# Try clean build
make clean && make pdf

# Verify all packages installed
tlmgr list --installed
```

---

## Production Workflow

### For Print Publishing

1. **Draft Review**
   ```bash
   make draft
   # Review build/Phoenix-Codex-v2.0.pdf
   ```

2. **Final Build**
   ```bash
   make final
   # 3-pass build with cross-refs and index
   ```

3. **Print Preparation**
   - Convert to CMYK if required
   - Verify bleed settings (0.125in standard)
   - Check spine width based on page count
   - Add printer marks if needed

4. **Digital Distribution**
   - Compress PDF for web: `gs -sDEVICE=pdfwrite ...`
   - Generate low-res preview version
   - Create EPUB version (via pandoc if needed)

---

## Advanced Features

### Cross-References

```latex
\label{law:recursive-identity}
See \autoref{law:recursive-identity} on page \pageref{law:recursive-identity}
```

### Index Generation

```latex
The \index{Recursive Operator}Recursive Operator...

% In preamble:
\usepackage{makeidx}
\makeindex

% At end:
\printindex
```

### Bibliography

```latex
\cite{category-theory-2020}

% At end:
\bibliography{references}
\bibliographystyle{plain}
```

---

## Next Steps

1. Populate chapter `.tex` files with content from markdown
2. Test build locally with `make pdf`
3. Customize colors/fonts to taste
4. Generate sigil cards for ceremonial use
5. Submit final PDF to print-on-demand service

---

## References

- [LaTeX Documentation](https://www.latex-project.org/help/documentation/)
- [XeLaTeX Guide](https://www.overleaf.com/learn/latex/XeLaTeX)
- [tcolorbox Manual](https://ctan.org/pkg/tcolorbox)
- [memoir Class](https://ctan.org/pkg/memoir) (alternative to book)

---

*"The sigil rendered in ink becomes ceremony; the PDF printed becomes scripture."*
