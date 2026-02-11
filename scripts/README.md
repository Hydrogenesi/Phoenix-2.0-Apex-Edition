# Phoenix 2.0 Build Scripts

This directory contains shell scripts for building and distributing the Phoenix 2.0 Codex documentation.

## Scripts

### 🔨 build-pdf.sh

Converts Markdown documentation to a LaTeX-formatted PDF codex with a custom cover page.

**Usage:**
```bash
./scripts/build-pdf.sh [build_dir] [output_dir]
```

**Features:**
- Generates a Codex-style cover page with Phoenix symbol
- Compiles all operators, laws, and rituals into a single PDF
- Creates table of contents
- Formats with LaTeX for professional output

**Requirements:**
- `pandoc` - Document converter
- `texlive-xetex` - XeLaTeX engine
- `texlive-latex-extra` - Additional LaTeX packages

**Output:**
- `output/Phoenix-2.0-Codex.pdf` - Complete Phoenix 2.0 documentation

---

### 🎨 convert-svg.sh

Converts the PDF codex to SVG format for web display.

**Usage:**
```bash
./scripts/convert-svg.sh [pdf_file] [output_dir]
```

**Features:**
- Attempts multiple conversion methods (pdftocairo, inkscape, ImageMagick)
- Auto-installs missing dependencies when possible
- High-quality vector output

**Requirements** (one of):
- `pdftocairo` (recommended, from poppler-utils)
- `inkscape`
- `convert` (from ImageMagick)

**Output:**
- `output/Phoenix-2.0-Codex.svg` - SVG version of the codex

---

### 📚 sync-wiki.sh

Synchronizes documentation to wiki-compatible format and structure.

**Usage:**
```bash
./scripts/sync-wiki.sh [wiki_dir]
```

**Features:**
- Creates wiki directory structure
- Copies all documentation files
- Generates navigation sidebar
- Creates wiki footer

**Output:**
- `wiki/` directory with complete wiki-ready documentation
- `wiki/_Sidebar.md` - Navigation menu
- `wiki/_Footer.md` - Page footer

**Publishing to GitHub Wiki:**
```bash
cd wiki
git init
git add .
git commit -m "Sync Phoenix 2.0 documentation"
git remote add origin https://github.com/Hydrogenesi/Phoenix-2.0-Apex-Edition.wiki.git
git push -u origin master
```

---

## Quick Start

Run all build steps:
```bash
make all
```

Or run individual steps:
```bash
make pdf         # Build PDF only
make svg         # Convert PDF to SVG
make wiki-sync   # Prepare wiki files
```

## Dependencies Installation

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y pandoc texlive-xetex texlive-latex-extra poppler-utils
```

### macOS (Homebrew)
```bash
brew install pandoc basictex poppler
```

### Windows
1. Install [Pandoc](https://pandoc.org/installing.html)
2. Install [MiKTeX](https://miktex.org/)
3. Install [Poppler](https://blog.alivate.com.au/poppler-windows/)

## Troubleshooting

### PDF Generation Fails
- Ensure pandoc is installed: `pandoc --version`
- Install LaTeX: `sudo apt-get install texlive-xetex texlive-latex-extra`
- Check log files in `build/` directory

### SVG Conversion Fails
- Install poppler-utils: `sudo apt-get install poppler-utils`
- Alternative: `sudo apt-get install inkscape`

### Permission Denied
- Make scripts executable: `chmod +x scripts/*.sh`

## Build Pipeline

The complete build pipeline follows this flow:

```
Markdown Sources → LaTeX → PDF → SVG
                                  ↓
                           Wiki Structure
```

1. **Markdown Sources**: Individual .md files for operators, laws, and rituals
2. **LaTeX**: Combined and formatted with custom cover page
3. **PDF**: Professional codex document
4. **SVG**: Web-ready vector graphics
5. **Wiki**: Organized documentation structure

---

**Made with 🔥 by the Phoenix Collective**
