#!/bin/bash
# Compile LaTeX Documents for Phoenix 2.0 Apex Edition
# Full LaTeX build automation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$(dirname "$SCRIPT_DIR")"
LATEX_DIR="$ASSETS_DIR/latex"
BUILD_DIR="$LATEX_DIR/build"

echo "Phoenix 2.0 Apex Edition - LaTeX Compiler"
echo "=========================================="
echo ""

# Check prerequisites
check_prerequisites() {
    echo "Checking prerequisites..."
    
    if ! command -v xelatex &> /dev/null; then
        echo "ERROR: xelatex not found"
        echo "Install with: sudo apt-get install texlive-xetex"
        exit 1
    fi
    
    # Check for fonts (best effort)
    if ! fc-list | grep -qi "EB Garamond"; then
        echo "WARNING: EB Garamond font not found"
        echo "Install with: sudo apt-get install fonts-ebgaramond"
    fi
    
    if ! fc-list | grep -qi "Fira Code"; then
        echo "WARNING: Fira Code font not found"
        echo "Install with: sudo apt-get install fonts-firacode"
    fi
    
    echo "Prerequisites OK"
    echo ""
}

# Build main codex
build_codex() {
    echo "Building main codex..."
    cd "$BUILD_DIR"
    
    # Run make
    if [ -f "Makefile" ]; then
        make final
    else
        echo "ERROR: Makefile not found in $BUILD_DIR"
        exit 1
    fi
    
    echo ""
}

# Main execution
main() {
    check_prerequisites
    
    case "${1:-all}" in
        all|codex)
            build_codex
            ;;
        draft)
            cd "$BUILD_DIR"
            make draft
            ;;
        clean)
            cd "$BUILD_DIR"
            make clean
            ;;
        help)
            echo "Usage: $0 [all|codex|draft|clean|help]"
            echo ""
            echo "Commands:"
            echo "  all    - Build everything (default)"
            echo "  codex  - Build main codex PDF"
            echo "  draft  - Quick draft build"
            echo "  clean  - Clean build artifacts"
            echo "  help   - Show this help"
            ;;
        *)
            echo "Unknown command: $1"
            echo "Run '$0 help' for usage"
            exit 1
            ;;
    esac
    
    echo "Build complete!"
}

main "$@"
