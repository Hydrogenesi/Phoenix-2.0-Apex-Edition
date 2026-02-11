# Phoenix 2.0 Apex Edition - Build Pipeline
# This Makefile coordinates the build of documentation from Markdown to PDF to SVG

SHELL := /bin/bash
.SHELLFLAGS := -e -o pipefail -c

# Directories
BUILD_DIR := build
SCRIPTS_DIR := scripts
OUTPUT_DIR := output
WIKI_DIR := wiki

# Main documentation files
MAIN_DOCS := README.md \
	operators/genesis.md \
	operators/harmonic.md \
	operators/recursive.md \
	operators/apex.md \
	operators/void.md \
	operators/mirror.md \
	operators/convergence.md \
	operators/divergence.md \
	laws/conservation.md \
	laws/symmetry.md \
	laws/recursion.md \
	laws/emergence.md \
	laws/duality.md \
	rituals/invocation.md \
	rituals/recursion-cycles.md \
	rituals/apex-formation.md

# Output files
PDF_OUTPUT := $(OUTPUT_DIR)/Phoenix-2.0-Codex.pdf
SVG_OUTPUT := $(OUTPUT_DIR)/Phoenix-2.0-Codex.svg

.PHONY: all pdf svg wiki-sync clean help setup

# Default target
all: setup pdf svg

# Display help information
help:
	@echo "Phoenix 2.0 Apex Edition - Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  make all        - Build PDF and SVG (default)"
	@echo "  make pdf        - Generate PDF codex from markdown"
	@echo "  make svg        - Convert PDF to SVG format"
	@echo "  make wiki-sync  - Synchronize documentation to wiki"
	@echo "  make clean      - Remove all build artifacts"
	@echo "  make setup      - Create required directories"
	@echo "  make help       - Display this help message"

# Create required directories
setup:
	@mkdir -p $(BUILD_DIR) $(OUTPUT_DIR) $(WIKI_DIR) $(SCRIPTS_DIR)
	@echo "✓ Directories created"

# Build PDF codex from markdown sources
pdf: setup
	@echo "🔥 Building Phoenix 2.0 Codex PDF..."
	@$(SCRIPTS_DIR)/build-pdf.sh $(BUILD_DIR) $(OUTPUT_DIR)
	@echo "✓ PDF generated: $(PDF_OUTPUT)"

# Convert PDF to SVG format
svg: pdf
	@echo "🎨 Converting PDF to SVG..."
	@$(SCRIPTS_DIR)/convert-svg.sh $(PDF_OUTPUT) $(OUTPUT_DIR)
	@echo "✓ SVG generated: $(SVG_OUTPUT)"

# Synchronize documentation to wiki
wiki-sync: setup
	@echo "📚 Synchronizing to wiki..."
	@$(SCRIPTS_DIR)/sync-wiki.sh $(WIKI_DIR)
	@echo "✓ Wiki synchronized"

# Clean all build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR) $(OUTPUT_DIR)
	@echo "✓ Clean complete"

# Clean including wiki directory
clean-all: clean
	@rm -rf $(WIKI_DIR)
	@echo "✓ Full clean complete"
