#!/bin/bash
# sync-wiki.sh - Synchronize Phoenix 2.0 documentation to wiki format
# Usage: sync-wiki.sh <wiki_dir>

set -euo pipefail

WIKI_DIR="${1:-wiki}"

echo "📚 Phoenix 2.0 Wiki Synchronization"
echo "===================================="

# Create wiki directory structure
echo "📁 Creating wiki directory structure..."
mkdir -p "$WIKI_DIR"/{operators,laws,rituals,guides}

# Copy and format main README
echo "📝 Syncing main documentation..."
cp README.md "$WIKI_DIR/Home.md"

# Sync operators
echo "🔧 Syncing operators..."
for op in operators/*.md; do
    filename=$(basename "$op")
    cp "$op" "$WIKI_DIR/operators/$filename"
done

# Sync laws
echo "⚖️  Syncing universal laws..."
for law in laws/*.md; do
    filename=$(basename "$law")
    cp "$law" "$WIKI_DIR/laws/$filename"
done

# Sync rituals
echo "🔮 Syncing rituals..."
for ritual in rituals/*.md; do
    filename=$(basename "$ritual")
    cp "$ritual" "$WIKI_DIR/rituals/$filename"
done

# Sync guides
echo "📖 Syncing guides..."
for guide in guides/*.md; do
    filename=$(basename "$guide")
    cp "$guide" "$WIKI_DIR/guides/$filename"
done

# Create wiki sidebar
echo "📋 Creating wiki navigation..."
cat > "$WIKI_DIR/_Sidebar.md" << 'EOF'
# Phoenix 2.0 Navigation

## 🏠 [Home](Home)

## 🔧 Operators
- [Genesis ⊕](operators/genesis)
- [Harmonic ⊗](operators/harmonic)
- [Recursive ⊛](operators/recursive)
- [Apex △](operators/apex)
- [Void ⊝](operators/void)
- [Mirror ⊞](operators/mirror)
- [Convergence ⊳](operators/convergence)
- [Divergence ⊲](operators/divergence)

## ⚖️ Universal Laws
- [Conservation](laws/conservation)
- [Symmetry](laws/symmetry)
- [Recursion](laws/recursion)
- [Emergence](laws/emergence)
- [Duality](laws/duality)

## 🔮 Rituals
- [Invocation](rituals/invocation)
- [Recursion Cycles](rituals/recursion-cycles)
- [Apex Formation](rituals/apex-formation)

## 📖 Guides
- [Quickstart](guides/quickstart)
- [Glossary](guides/glossary)
EOF

# Create wiki footer
cat > "$WIKI_DIR/_Footer.md" << 'EOF'
---
**Phoenix 2.0 — Apex Edition** | Made with 🔥 by the Phoenix Collective
EOF

echo ""
echo "✨ Wiki synchronization complete!"
echo "Wiki directory: $WIKI_DIR"
echo ""
echo "To publish to GitHub Wiki:"
echo "  cd $WIKI_DIR"
echo "  git init"
echo "  git add ."
echo "  git commit -m 'Sync Phoenix 2.0 documentation'"
echo "  git remote add origin <wiki-repo-url>"
echo "  git push -u origin master"
