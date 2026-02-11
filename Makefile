# ============================
#  TRIAD SYSTEM — PRODUCTION
# ============================

.PHONY: help pdf sigil-cards svg clean

# Default target
help:
	@echo "Phoenix 2.0 Apex Edition — TRIAD SYSTEM"
	@echo ""
	@echo "Available targets:"
	@echo "  pdf          - Build all LaTeX documents"
	@echo "  sigil-cards  - Generate sigil cards"
	@echo "  svg          - Export SVG assets"
	@echo "  clean        - Clean build artifacts"
	@echo "  help         - Show this help message"

# Build all LaTeX documents
pdf:
	@echo "Building PDF Codex artifacts..."
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -pdf -interaction=nonstopmode -output-directory=build codex/*.tex; \
	else \
		echo "Error: latexmk is not installed"; \
		echo "Please install LaTeX and latexmk to build PDF documents"; \
		exit 1; \
	fi

# Generate sigil cards (ASCII → PNG/SVG via your chosen pipeline)
sigil-cards:
	@echo "Generating sigil cards..."
	./scripts/generate_sigil_cards.sh

# Export SVG assets (diagrams, sigils, topology maps)
svg:
	@echo "Exporting SVG assets..."
	./scripts/export_svg.sh

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -C -output-directory=build codex/*.tex; \
	else \
		echo "  latexmk not found, skipping LaTeX cleanup"; \
		rm -f codex/*.aux codex/*.fdb_latexmk codex/*.fls codex/*.log codex/*.out codex/*.synctex.gz codex/*.toc; \
	fi
	rm -rf build/*
