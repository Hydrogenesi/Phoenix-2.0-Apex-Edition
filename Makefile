# Makefile for Phoenix 2.0 — Apex Edition Codex
# Production build pipeline

.PHONY: all pdf sigils svg clean help

# Default target
all: sigils svg pdf

# Generate PDF with LaTeX cover page
pdf:
	@echo "🔥 Generating Codex PDF..."
	@if command -v pdflatex >/dev/null 2>&1; then \
		cd docs && pdflatex -interaction=nonstopmode cover.tex && \
		echo "✓ PDF cover generated: docs/cover.pdf"; \
	else \
		echo "⚠ pdflatex not found. Skipping PDF generation."; \
		echo "  Install: sudo apt-get install texlive-latex-base"; \
	fi

# Generate individual sigil cards
sigils:
	@echo "🔺 Generating sigil cards..."
	@bash scripts/generate-sigils.sh
	@echo "✓ Sigils generated in build/sigils/"

# Export Mermaid diagrams to SVG
svg:
	@echo "🗺️  Exporting diagrams to SVG..."
	@bash scripts/export-svg.sh
	@echo "✓ SVG files generated in build/svg/"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/
	@rm -f docs/cover.pdf docs/cover.aux docs/cover.log
	@echo "✓ Clean complete"

# Show help
help:
	@echo "Phoenix 2.0 — Apex Edition Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  make all      - Build everything (sigils, svg, pdf)"
	@echo "  make pdf      - Generate PDF with LaTeX cover"
	@echo "  make sigils   - Generate individual sigil cards"
	@echo "  make svg      - Export Mermaid diagrams to SVG"
	@echo "  make clean    - Remove all build artifacts"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - pdflatex (for PDF generation)"
	@echo "  - mmdc (mermaid-cli, for SVG export)"
	@echo "  - bash (for scripts)"
