# Phoenix‑2.0‑Apex‑Edition — Build System
# v2.0.0 — Triadic Knot Release

.PHONY: all clean docs pdf wiki sigils test help
.PHONY: export-svg export-topology generate-sigils export-sigils
.PHONY: pdf-phoenix pdf-hydrogenesi pdf-thethird pdf-codex
.PHONY: wiki-sync wiki-deploy test-links test-structure
.PHONY: clean-deep init version dev-watch dev-serve
.PHONY: experimental-knot-viz experimental-operator-graph
.DEFAULT_GOAL := help

# ═══════════════════════════════════════════════════════════
# Directory Definitions
# ═══════════════════════════════════════════════════════════

PHOENIX_DIR    = Phoenix
HYDROGENESI_DIR = Hydrogenesi
THETHIRD_DIR   = TheThird
ATLASES_DIR    = Atlases
SIGILS_DIR     = sigils
SCRIPTS_DIR    = scripts
BUILD_DIR      = build
OUT_DIR        = out

# ═══════════════════════════════════════════════════════════
# Tool Definitions
# ═══════════════════════════════════════════════════════════

MMDC           = mmdc
PDFLATEX       = pdflatex
PYTHON         = python3

# ═══════════════════════════════════════════════════════════
# Primary Targets
# ═══════════════════════════════════════════════════════════

help:  ## Show this help message
	@echo "═══════════════════════════════════════════════════════════"
	@echo "  🔥 Phoenix 2.0 Apex Edition — Build System"
	@echo "  v2.0.0 — Triadic Knot Release"
	@echo "═══════════════════════════════════════════════════════════"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "═══════════════════════════════════════════════════════════"

all:  ## Build all documentation artifacts
	@echo "🔥 Building all Phoenix 2.0 documentation artifacts..."
	@$(MAKE) docs
	@$(MAKE) sigils
	@echo "✓ All artifacts built successfully!"

init:  ## Initialize build directories
	@echo "△ Initializing build directory structure..."
	@mkdir -p $(BUILD_DIR)/svg
	@mkdir -p $(BUILD_DIR)/topology
	@mkdir -p $(BUILD_DIR)/sigils/svg
	@mkdir -p $(BUILD_DIR)/sigils/png
	@mkdir -p $(BUILD_DIR)/wiki
	@mkdir -p $(OUT_DIR)
	@echo "✓ Build directories created:"
	@echo "  • $(BUILD_DIR)/svg"
	@echo "  • $(BUILD_DIR)/topology"
	@echo "  • $(BUILD_DIR)/sigils/{svg,png}"
	@echo "  • $(BUILD_DIR)/wiki"
	@echo "  • $(OUT_DIR)"

version:  ## Display version and architecture information
	@echo "═══════════════════════════════════════════════════════════"
	@echo "  Phoenix 2.0 Apex Edition"
	@echo "  Build System v2.0.0"
	@echo "  Triadic Knot Release"
	@echo "═══════════════════════════════════════════════════════════"
	@echo ""
	@echo "Architecture:"
	@echo "  • Substrate Layer:  Universal Laws (5)"
	@echo "  • Universal Layer:  Structural Axioms (7)"
	@echo "  • Apex Layer:       Triad Canon (5)"
	@echo "  • Engine Layer:     Phoenix & Hydrogenesi"
	@echo "  • Triad Layer:      Three Columns"
	@echo ""
	@echo "Components:"
	@echo "  • Operators:        8 primary transformation modes"
	@echo "  • Laws:             5 universal principles"
	@echo "  • Rituals:          Ceremonial invocation sequences"
	@echo "  • Atlases:          Topology and hierarchy diagrams"
	@echo ""

# ═══════════════════════════════════════════════════════════
# Documentation Build Targets
# ═══════════════════════════════════════════════════════════

docs:  ## Generate all documentation
	@echo "📖 Generating documentation artifacts..."
	@$(MAKE) export-svg
	@$(MAKE) export-topology
	@echo "✓ Documentation generation complete!"

export-svg:  ## Export Mermaid diagrams to SVG
	@echo "🔥 Exporting Mermaid diagrams to SVG..."
	@mkdir -p $(BUILD_DIR)/svg
	@if [ -f $(SCRIPTS_DIR)/export_svg.sh ]; then \
		bash $(SCRIPTS_DIR)/export_svg.sh $(ATLASES_DIR) $(BUILD_DIR)/svg; \
	else \
		echo "⚠️  Warning: $(SCRIPTS_DIR)/export_svg.sh not found"; \
		echo "   Diagram export skipped."; \
	fi

export-topology:  ## Generate Triadic Knot topology diagrams
	@echo "🔗 Generating Triadic Knot topology diagrams..."
	@mkdir -p $(BUILD_DIR)/topology
	@if [ -f $(SCRIPTS_DIR)/generate_topology.sh ]; then \
		bash $(SCRIPTS_DIR)/generate_topology.sh; \
	else \
		echo "⚠️  Warning: $(SCRIPTS_DIR)/generate_topology.sh not found"; \
		echo "   Topology generation skipped."; \
	fi

# ═══════════════════════════════════════════════════════════
# Sigil Generation Targets
# ═══════════════════════════════════════════════════════════

sigils:  ## Generate and export sigil artifacts
	@echo "△ Generating sigil artifacts..."
	@$(MAKE) generate-sigils
	@$(MAKE) export-sigils
	@echo "✓ Sigil generation complete!"

generate-sigils:  ## Generate ASCII sigil cards
	@echo "△ Generating ASCII sigil cards..."
	@mkdir -p $(BUILD_DIR)/sigils
	@if [ -f $(SCRIPTS_DIR)/generate_sigil_cards.sh ]; then \
		bash $(SCRIPTS_DIR)/generate_sigil_cards.sh; \
	else \
		echo "⚠️  Warning: $(SCRIPTS_DIR)/generate_sigil_cards.sh not found"; \
		echo "   Sigil card generation skipped."; \
	fi

export-sigils:  ## Export sigils to PNG/SVG (placeholder)
	@echo "△ Exporting sigils to PNG/SVG..."
	@mkdir -p $(BUILD_DIR)/sigils/svg
	@mkdir -p $(BUILD_DIR)/sigils/png
	@echo "⚠️  Sigil export not yet implemented."
	@echo "   Future: Convert ASCII sigils to vector graphics"

# ═══════════════════════════════════════════════════════════
# PDF Build Targets
# ═══════════════════════════════════════════════════════════

pdf:  ## Build all PDF documentation
	@echo "📄 Building all PDF documentation..."
	@$(MAKE) pdf-phoenix
	@$(MAKE) pdf-hydrogenesi
	@$(MAKE) pdf-thethird
	@$(MAKE) pdf-codex
	@echo "✓ PDF build complete!"

pdf-phoenix:  ## Build Phoenix documentation PDF
	@echo "🔥 Building Phoenix documentation PDF..."
	@mkdir -p $(OUT_DIR)
	@echo "⚠️  Phoenix PDF build not yet implemented."
	@echo "   Planned: LaTeX compilation pipeline"
	@echo "   Output: $(OUT_DIR)/Phoenix-2.0-Documentation.pdf"

pdf-hydrogenesi:  ## Build Hydrogenesi PDF
	@echo "🌊 Building Hydrogenesi documentation PDF..."
	@mkdir -p $(OUT_DIR)
	@echo "⚠️  Hydrogenesi PDF build not yet implemented."
	@echo "   Planned: LaTeX compilation pipeline"
	@echo "   Output: $(OUT_DIR)/Hydrogenesi-Documentation.pdf"

pdf-thethird:  ## Build The Third PDF
	@echo "🔗 Building The Third documentation PDF..."
	@mkdir -p $(OUT_DIR)
	@echo "⚠️  The Third PDF build not yet implemented."
	@echo "   Planned: LaTeX compilation pipeline"
	@echo "   Output: $(OUT_DIR)/TheThird-Documentation.pdf"

pdf-codex:  ## Build unified Codex PDF
	@echo "📚 Building unified Codex PDF..."
	@mkdir -p $(OUT_DIR)
	@echo "⚠️  Unified Codex PDF build not yet implemented."
	@echo "   Planned: Combine all documentation into single PDF"
	@echo "   Output: $(OUT_DIR)/Codex-Complete.pdf"

# ═══════════════════════════════════════════════════════════
# Wiki Synchronization Targets
# ═══════════════════════════════════════════════════════════

wiki:  ## Sync to GitHub Wiki
	@echo "📖 Syncing to GitHub Wiki..."
	@$(MAKE) wiki-sync
	@$(MAKE) wiki-deploy
	@echo "✓ Wiki sync complete!"

wiki-sync:  ## Prepare Wiki content
	@echo "📖 Preparing Wiki content..."
	@mkdir -p $(BUILD_DIR)/wiki
	@if [ -f $(SCRIPTS_DIR)/sync_wiki.sh ]; then \
		bash $(SCRIPTS_DIR)/sync_wiki.sh; \
	else \
		echo "⚠️  Warning: $(SCRIPTS_DIR)/sync_wiki.sh not found"; \
		echo "   Wiki sync skipped."; \
	fi

wiki-deploy:  ## Deploy to GitHub Wiki
	@echo "📖 Deploying to GitHub Wiki..."
	@echo "⚠️  Wiki deployment not yet implemented."
	@echo "   Planned: git push to wiki repository"
	@echo "   Manual: cd build/wiki && git push"

# ═══════════════════════════════════════════════════════════
# Testing and Validation Targets
# ═══════════════════════════════════════════════════════════

test:  ## Run validation tests
	@echo "🧪 Running validation tests..."
	@$(MAKE) test-links
	@$(MAKE) test-structure
	@echo "✓ All tests passed!"

test-links:  ## Validate internal links
	@echo "🔗 Testing internal links..."
	@mkdir -p $(BUILD_DIR)
	@if [ -f $(SCRIPTS_DIR)/test_links.sh ]; then \
		bash $(SCRIPTS_DIR)/test_links.sh; \
	else \
		echo "⚠️  Warning: $(SCRIPTS_DIR)/test_links.sh not found"; \
		echo "   Link validation skipped."; \
	fi

test-structure:  ## Validate repository structure
	@echo "🏗️  Validating repository structure..."
	@echo "Checking required directories..."
	@test -d operators || (echo "✗ Missing: operators/" && exit 1)
	@echo "  ✓ operators/"
	@test -d laws || (echo "✗ Missing: laws/" && exit 1)
	@echo "  ✓ laws/"
	@test -d rituals || (echo "✗ Missing: rituals/" && exit 1)
	@echo "  ✓ rituals/"
	@test -d guides || (echo "✗ Missing: guides/" && exit 1)
	@echo "  ✓ guides/"
	@test -d $(ATLASES_DIR) || (echo "✗ Missing: $(ATLASES_DIR)/" && exit 1)
	@echo "  ✓ $(ATLASES_DIR)/"
	@echo "Checking core documentation files..."
	@test -f README.md || (echo "✗ Missing: README.md" && exit 1)
	@echo "  ✓ README.md"
	@test -f LICENSE || (echo "✗ Missing: LICENSE" && exit 1)
	@echo "  ✓ LICENSE"
	@echo "✓ Repository structure is valid!"

# ═══════════════════════════════════════════════════════════
# Cleanup Targets
# ═══════════════════════════════════════════════════════════

clean:  ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)/*
	@rm -rf $(OUT_DIR)/*
	@echo "✓ Build artifacts cleaned!"
	@echo "  • Removed: $(BUILD_DIR)/*"
	@echo "  • Removed: $(OUT_DIR)/*"

clean-deep:  ## Deep clean including LaTeX aux files
	@echo "🧹 Performing deep clean..."
	@$(MAKE) clean
	@find . -type f -name "*.aux" -delete
	@find . -type f -name "*.log" -delete
	@find . -type f -name "*.toc" -delete
	@find . -type f -name "*.out" -delete
	@find . -type f -name "*.synctex.gz" -delete
	@echo "✓ Deep clean complete!"
	@echo "  • Removed LaTeX auxiliary files"

# ═══════════════════════════════════════════════════════════
# Development Targets
# ═══════════════════════════════════════════════════════════

dev-watch:  ## Watch for changes and rebuild
	@echo "👀 Watching for changes..."
	@if command -v inotifywait >/dev/null 2>&1; then \
		echo "Monitoring: operators/, laws/, rituals/, guides/, $(ATLASES_DIR)/"; \
		while true; do \
			inotifywait -r -e modify,create,delete \
				operators/ laws/ rituals/ guides/ $(ATLASES_DIR)/ 2>/dev/null && \
			echo "🔄 Changes detected, rebuilding..." && \
			$(MAKE) docs; \
		done \
	else \
		echo "⚠️  inotifywait not found. Install inotify-tools:"; \
		echo "   Ubuntu/Debian: sudo apt-get install inotify-tools"; \
		echo "   macOS: brew install fswatch"; \
	fi

dev-serve:  ## Serve documentation locally
	@echo "🌐 Starting local documentation server..."
	@echo "Server running at: http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@cd . && $(PYTHON) -m http.server 8000

# ═══════════════════════════════════════════════════════════
# Experimental Targets
# ═══════════════════════════════════════════════════════════

experimental-knot-viz:  ## Interactive Triadic Knot visualization (experimental)
	@echo "🔮 Experimental: Interactive Triadic Knot Visualization"
	@echo "⚠️  Not yet implemented."
	@echo ""
	@echo "Planned features:"
	@echo "  • 3D WebGL knot rendering"
	@echo "  • Interactive corridor navigation"
	@echo "  • Real-time operator application"
	@echo "  • Symmetry axis visualization"
	@echo ""
	@echo "Recommended tools: Three.js, D3.js, WebGL"

experimental-operator-graph:  ## Operator dependency graph (experimental)
	@echo "🔮 Experimental: Operator Dependency Graph"
	@echo "⚠️  Not yet implemented."
	@echo ""
	@echo "Planned features:"
	@echo "  • Visual operator relationship graph"
	@echo "  • Law enforcement visualization"
	@echo "  • Ritual sequence diagrams"
	@echo "  • Emergence pattern detection"
	@echo ""
	@echo "Recommended tools: GraphViz, D3.js, Cytoscape"
