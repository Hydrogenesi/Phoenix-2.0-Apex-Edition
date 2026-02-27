# Triad System Makefile
# Build automation for LaTeX codex and sigil generation

# Configuration
LATEX = pdflatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error
CODEX_DIR = codex
SCRIPTS_DIR = scripts
BUILD_DIR = build
OUTPUT_DIR = output

# Source files
CODEX_MAIN = $(CODEX_DIR)/codex.tex
CODEX_SOURCES = $(wildcard $(CODEX_DIR)/*.tex)

# Output files
CODEX_PDF = $(OUTPUT_DIR)/codex.pdf

# Phony targets
.PHONY: all codex sigils clean help

# Default target
all: codex sigils

# Help target
help:
	@echo "Triad System Build Automation"
	@echo ""
	@echo "Available targets:"
	@echo "  all       - Build codex and generate sigils (default)"
	@echo "  codex     - Compile LaTeX codex to PDF"
	@echo "  sigils    - Generate sigil card SVGs"
	@echo "  clean     - Remove build artifacts"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - pdflatex for codex compilation"
	@echo "  - bash for script execution"
	@echo "  - inkscape or similar for SVG export (optional)"

# Build codex from LaTeX sources
codex: $(CODEX_PDF)

$(CODEX_PDF): $(CODEX_SOURCES) | $(BUILD_DIR) $(OUTPUT_DIR)
	@echo "Building LaTeX codex..."
	cd $(CODEX_DIR) && $(LATEX) $(LATEX_FLAGS) -output-directory=../$(BUILD_DIR) codex.tex
	@echo "Running second pass for references..."
	cd $(CODEX_DIR) && $(LATEX) $(LATEX_FLAGS) -output-directory=../$(BUILD_DIR) codex.tex
	@mv $(BUILD_DIR)/codex.pdf $(OUTPUT_DIR)/codex.pdf
	@echo "Codex compiled successfully: $(CODEX_PDF)"

# Generate sigil cards
sigils: | $(OUTPUT_DIR)
	@echo "Generating sigil cards..."
	@bash $(SCRIPTS_DIR)/generate_sigil_cards.sh
	@echo "Sigil cards generated in $(OUTPUT_DIR)/sigils/"

# Export SVG diagrams
svg: | $(OUTPUT_DIR)
	@echo "Exporting diagrams to SVG..."
	@bash $(SCRIPTS_DIR)/export_svg.sh
	@echo "SVG diagrams exported to $(OUTPUT_DIR)/svg/"

# Create build directories
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(OUTPUT_DIR)/sigils
	@mkdir -p $(OUTPUT_DIR)/svg

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@rm -rf $(OUTPUT_DIR)
	@echo "Clean complete."

# Deep clean (including editor backups)
distclean: clean
	@echo "Deep cleaning..."
	@find . -name "*.aux" -delete
	@find . -name "*.log" -delete
	@find . -name "*.toc" -delete
	@find . -name "*.out" -delete
	@find . -name "*~" -delete
	@echo "Deep clean complete."
