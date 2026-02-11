# Phoenix 2.0 Apex Edition - LaTeX Build System
# Professional document generation

# ============================================================
# CONFIGURATION
# ============================================================

LATEX = xelatex
LATEXFLAGS = -interaction=nonstopmode -halt-on-error

TEMPLATE_DIR = ../templates
CHAPTER_DIR = ../chapters
APPENDIX_DIR = ../appendices
BUILD_DIR = .

# Main document
MAIN_DOC = $(TEMPLATE_DIR)/codex-main.tex
MAIN_PDF = Phoenix-Codex-v2.0.pdf

# Card template
CARD_TEMPLATE = $(TEMPLATE_DIR)/sigil-card.tex
CARDS_DIR = cards

# ============================================================
# MAIN TARGETS
# ============================================================

.PHONY: all pdf draft final clean distclean sigil-cards help

all: pdf

pdf: $(MAIN_PDF)

# Quick draft (single pass)
draft:
	@echo "Building draft..."
	$(LATEX) $(LATEXFLAGS) $(MAIN_DOC)
	@mv codex-main.pdf $(MAIN_PDF) 2>/dev/null || true

# Production build (3 passes for cross-refs)
final: clean
	@echo "Building final version (pass 1/3)..."
	$(LATEX) $(LATEXFLAGS) $(MAIN_DOC)
	@echo "Building final version (pass 2/3)..."
	$(LATEX) $(LATEXFLAGS) $(MAIN_DOC)
	@echo "Building final version (pass 3/3)..."
	$(LATEX) $(LATEXFLAGS) $(MAIN_DOC)
	@mv codex-main.pdf $(MAIN_PDF) 2>/dev/null || true
	@echo "Final build complete: $(MAIN_PDF)"

# Generate all sigil cards
sigil-cards: $(CARDS_DIR)
	@echo "Generating sigil cards..."
	@echo "Building Genesis card..."
	$(LATEX) $(LATEXFLAGS) $(CARD_TEMPLATE)
	@mv sigil-card.pdf $(CARDS_DIR)/genesis-operator.pdf 2>/dev/null || true
	@echo "Sigil cards generated in $(CARDS_DIR)/"
	@echo "Note: Customize card content by editing $(CARD_TEMPLATE)"

# ============================================================
# HELPER TARGETS
# ============================================================

# Create cards directory
$(CARDS_DIR):
	mkdir -p $(CARDS_DIR)

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.idx *.ind *.ilg
	rm -f *.fls *.fdb_latexmk *.synctex.gz
	rm -f codex-main.pdf sigil-card.pdf

# Remove all generated files
distclean: clean
	rm -f $(MAIN_PDF)
	rm -rf $(CARDS_DIR)
	@echo "All generated files removed"

# ============================================================
# INFORMATION
# ============================================================

help:
	@echo "Phoenix 2.0 Apex Edition - LaTeX Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  make pdf          - Build complete codex (default)"
	@echo "  make draft        - Quick draft build (1 pass)"
	@echo "  make final        - Production build (3 passes)"
	@echo "  make sigil-cards  - Generate operator/law cards"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make distclean    - Remove all generated files"
	@echo "  make help         - Show this help"
	@echo ""
	@echo "Requirements:"
	@echo "  - XeLaTeX (texlive-xetex)"
	@echo "  - EB Garamond font"
	@echo "  - Fira Code font"
	@echo "  - Cinzel font"
	@echo ""
	@echo "Install on Ubuntu/Debian:"
	@echo "  sudo apt-get install texlive-xetex fonts-ebgaramond"
	@echo "  sudo apt-get install fonts-firacode fonts-cinzel"

# ============================================================
# BUILD RULES
# ============================================================

$(MAIN_PDF): $(MAIN_DOC)
	@echo "Building codex..."
	$(LATEX) $(LATEXFLAGS) $(MAIN_DOC)
	$(LATEX) $(LATEXFLAGS) $(MAIN_DOC)
	@mv codex-main.pdf $(MAIN_PDF) 2>/dev/null || true
	@echo "Build complete: $(MAIN_PDF)"

# ============================================================
# PHONY TARGETS
# ============================================================

.DEFAULT_GOAL := help
