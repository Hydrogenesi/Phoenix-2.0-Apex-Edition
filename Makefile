# Phoenix 2.0 Apex Edition - Master Build System
# Build all production assets

# ============================================================
# CONFIGURATION
# ============================================================

ASSETS_DIR = assets
LATEX_DIR = $(ASSETS_DIR)/latex/build
SCRIPTS_DIR = $(ASSETS_DIR)/scripts

# ============================================================
# MAIN TARGETS
# ============================================================

.PHONY: all pdf sigil-cards svg clean distclean help

all: help

# Build all LaTeX documents
pdf:
	@echo "Building LaTeX documents..."
	cd $(LATEX_DIR) && $(MAKE) final

# Generate sigil cards
sigil-cards:
	@echo "Generating sigil cards..."
	bash $(SCRIPTS_DIR)/generate-sigil-cards.sh

# Export SVG assets
svg:
	@echo "Exporting SVG assets..."
	bash $(SCRIPTS_DIR)/export-svg.sh

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	cd $(LATEX_DIR) && $(MAKE) clean

# Remove all generated files
distclean:
	@echo "Removing all generated files..."
	cd $(LATEX_DIR) && $(MAKE) distclean

# ============================================================
# CONVENIENCE TARGETS
# ============================================================

# Quick draft build
draft:
	@echo "Building quick draft..."
	cd $(LATEX_DIR) && $(MAKE) draft

# Build everything
build-all: pdf sigil-cards
	@echo ""
	@echo "All assets built successfully!"
	@echo ""
	@echo "Output locations:"
	@echo "  - Main codex: $(LATEX_DIR)/Phoenix-Codex-v2.0.pdf"
	@echo "  - Sigil cards: $(LATEX_DIR)/cards/"
	@echo ""

# ============================================================
# INFORMATION
# ============================================================

help:
	@echo "Phoenix 2.0 Apex Edition - Master Build System"
	@echo "=============================================="
	@echo ""
	@echo "Available targets:"
	@echo "  make pdf          - Build complete codex PDF"
	@echo "  make draft        - Quick draft build"
	@echo "  make sigil-cards  - Generate operator/law cards"
	@echo "  make svg          - Export SVG assets"
	@echo "  make build-all    - Build PDF and cards"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make distclean    - Remove all generated files"
	@echo "  make help         - Show this help (default)"
	@echo ""
	@echo "Documentation Structure:"
	@echo "  docs/             - Core 13 components + supplementary"
	@echo "  laws/             - Three-layer law system"
	@echo "  operators/        - Eight operator specifications"
	@echo "  engines/          - Phoenix and Hydrogenesi engines"
	@echo "  triad/            - Three-column architecture"
	@echo "  sigils/           - Symbolic systems"
	@echo "  atlases/          - Visual documentation"
	@echo "  rituals/          - Ceremonial patterns"
	@echo "  architecture/     - Framework analysis"
	@echo "  assets/           - Production files (LaTeX, SVG, scripts)"
	@echo ""
	@echo "Quick Reference:"
	@echo "  README.md                  - Main entry point"
	@echo "  SEVEN_UNIVERSAL_LAWS.md    - Quick law reference"
	@echo "  assets/SIGIL_ATLAS.md      - Single-page ASCII atlas"
	@echo "  docs/INDEX.md              - Master documentation index"
	@echo ""
	@echo "Build Requirements:"
	@echo "  - XeLaTeX (texlive-xetex)"
	@echo "  - EB Garamond, Cinzel, Fira Code fonts"
	@echo "  - bash (for build scripts)"
	@echo ""
	@echo "Installation (Ubuntu/Debian):"
	@echo "  sudo apt-get install texlive-xetex"
	@echo "  sudo apt-get install fonts-ebgaramond fonts-cinzel fonts-firacode"
	@echo ""
	@echo "For complete documentation, see assets/latex/README.md"

# ============================================================
# PHONY TARGETS
# ============================================================

.DEFAULT_GOAL := help
