# Build System Documentation

This document describes the TRIAD SYSTEM build infrastructure for Phoenix 2.0 Apex Edition.

## Overview

The build system provides targets for generating various artifacts from the Phoenix 2.0 documentation:
- PDF codex documents from LaTeX sources
- Sigil card assets from operator definitions
- SVG diagrams and topology maps

## Prerequisites

### Required
- Bash shell
- Make

### Optional
- LaTeX distribution with `latexmk` (for PDF generation)
- Image processing tools (for advanced sigil card generation)

## Usage

### Build All Targets

Run the help command to see available targets:
```bash
make help
```

### Build PDF Documents

Generate PDF codex documents from LaTeX sources:
```bash
make pdf
```

**Note:** Requires LaTeX and latexmk to be installed.

### Generate Sigil Cards

Extract and process operator sigils:
```bash
make sigil-cards
```

Output location: `build/sigils/`

### Export SVG Assets

Generate SVG diagrams and topology maps:
```bash
make svg
```

Output location: `build/svg/`

### Clean Build Artifacts

Remove all generated files:
```bash
make clean
```

## Directory Structure

```
Phoenix-2.0-Apex-Edition/
├── Makefile              # Main build file
├── codex/                # LaTeX source files
│   └── phoenix_codex.tex
├── scripts/              # Build scripts
│   ├── generate_sigil_cards.sh
│   └── export_svg.sh
└── build/                # Generated artifacts (excluded from git)
    ├── sigils/
    └── svg/
```

## Scripts

### generate_sigil_cards.sh

Processes operator markdown files to extract sigil information.
- Input: `operators/*.md`
- Output: `build/sigils/*.txt`

### export_svg.sh

Generates SVG assets from documentation sources.
- Input: `operators/*.md`, `rituals/*.md`, `Atlases/*.md`
- Output: `build/svg/`

## Customization

The scripts are designed to be extensible. You can modify them to:
- Add custom image processing pipelines
- Integrate with vector graphics tools
- Generate additional artifact types
- Customize output formats

## Troubleshooting

### LaTeX not installed

If you see "latexmk is not installed", install a LaTeX distribution:
- **Ubuntu/Debian**: `sudo apt-get install texlive-full latexmk`
- **macOS**: Install MacTeX from https://www.tug.org/mactex/
- **Windows**: Install MiKTeX from https://miktex.org/

### Scripts not executable

If scripts fail to run, ensure they are executable:
```bash
chmod +x scripts/*.sh
```

### Build directory issues

If the build directory has permission issues, recreate it:
```bash
rm -rf build/
mkdir build/
```

## Contributing

When adding new build targets:
1. Update the Makefile with the new target
2. Add any required scripts to the `scripts/` directory
3. Update this documentation
4. Ensure build artifacts are added to `.gitignore`
