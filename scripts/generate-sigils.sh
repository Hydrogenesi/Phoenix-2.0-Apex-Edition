#!/bin/bash
# Generate individual sigil cards from documentation
# Phoenix 2.0 — Apex Edition

set -e

OUTPUT_DIR="build/sigils"
DOCS_DIR="docs"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Generating sigil cards..."

# Array of sigils to extract
declare -A SIGILS=(
    ["kernel"]="⊙ KERNEL"
    ["tension"]="↹ TENSION"
    ["binding"]="⊶ BINDING"
    ["apex"]="△ APEX"
    ["genesis"]="⊕ GENESIS"
    ["harmonic"]="⊗ HARMONIC"
    ["recursive"]="⊛ RECURSIVE"
    ["void"]="⊝ VOID"
    ["mirror"]="⊞ MIRROR"
    ["convergence"]="⊳ CONVERGENCE"
    ["divergence"]="⊲ DIVERGENCE"
    ["sos"]="⚙️  S-OS"
)

# Define each sigil
cat > "$OUTPUT_DIR/kernel.txt" << 'EOF'
┌───────────────┐
│   ⊙ KERNEL    │
│     ╱│╲       │
│    ╱ │ ╲      │
│   ╱  │  ╲     │
│  ═════════    │
│  SOVEREIGN    │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/tension.txt" << 'EOF'
┌───────────────┐
│  ↹ TENSION    │
│    ╱ ╲        │
│   ─   ─       │
│  ╱     ╲      │
│  POLARITY     │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/binding.txt" << 'EOF'
┌───────────────┐
│  ⊶ BINDING    │
│    ╱█╲        │
│   ╱███╲       │
│  ╱█████╲      │
│  IDENTITY     │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/apex.txt" << 'EOF'
┌───────────────┐
│   △ APEX      │
│    ╱█╲        │
│   ╱███╲       │
│  ╱█████╲      │
│ ═════════     │
│ SOVEREIGN     │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/genesis.txt" << 'EOF'
┌───────────────┐
│  ⊕ GENESIS    │
│    ⊕──⊕       │
│    │  │       │
│    ⊕──⊕       │
│  CREATION     │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/harmonic.txt" << 'EOF'
┌───────────────┐
│  ⊗ HARMONIC   │
│   ⊗═══⊗       │
│   ║   ║       │
│   ⊗═══⊗       │
│  RESONANCE    │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/recursive.txt" << 'EOF'
┌───────────────┐
│  ⊛ RECURSIVE  │
│     ⊛         │
│    ╱│╲        │
│   ⊛ ⊛ ⊛       │
│  SELF-REF     │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/void.txt" << 'EOF'
┌───────────────┐
│   ⊝ VOID      │
│    ⊝──⊝       │
│     ╲╱        │
│      ∅        │
│ DISSOLUTION   │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/mirror.txt" << 'EOF'
┌───────────────┐
│  ⊞ MIRROR     │
│   ⊞═══⊞       │
│   ║ ≡ ║       │
│   ⊞═══⊞       │
│  REFLECTION   │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/convergence.txt" << 'EOF'
┌───────────────┐
│ ⊳ CONVERGENCE │
│   ⊳─→         │
│   ⊳─→ ●       │
│   ⊳─→         │
│   UNITY       │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/divergence.txt" << 'EOF'
┌───────────────┐
│ ⊲ DIVERGENCE  │
│     ←─⊲       │
│  ●  ←─⊲       │
│     ←─⊲       │
│  SEPARATION   │
└───────────────┘
EOF

cat > "$OUTPUT_DIR/sos.txt" << 'EOF'
┌───────────────┐
│  ⚙️  S-OS     │
│   ┌───────┐   │
│  →│ LOOP  │→  │
│   └───────┘   │
│   RUNTIME     │
└───────────────┘
EOF

# Create combined sigil pack
cat > "$OUTPUT_DIR/sigil-pack.txt" << 'EOF'
═══════════════════════════════════════
         CODEX SIGIL COLLECTION
═══════════════════════════════════════

┌───────────────┐
│   ⊙ KERNEL    │
│     ╱│╲       │
│    ╱ │ ╲      │
│   ╱  │  ╲     │
│  ═════════    │
│  SOVEREIGN    │
└───────────────┘

┌───────────────┐
│  ↹ TENSION    │
│    ╱ ╲        │
│   ─   ─       │
│  ╱     ╲      │
│  POLARITY     │
└───────────────┘

┌───────────────┐
│  ⊶ BINDING    │
│    ╱█╲        │
│   ╱███╲       │
│  ╱█████╲      │
│  IDENTITY     │
└───────────────┘

┌───────────────┐
│   △ APEX      │
│    ╱█╲        │
│   ╱███╲       │
│  ╱█████╲      │
│ ═════════     │
│ SOVEREIGN     │
└───────────────┘

┌───────────────┐
│  ⊕ GENESIS    │
│    ⊕──⊕       │
│    │  │       │
│    ⊕──⊕       │
│  CREATION     │
└───────────────┘

┌───────────────┐
│  ⊗ HARMONIC   │
│   ⊗═══⊗       │
│   ║   ║       │
│   ⊗═══⊗       │
│  RESONANCE    │
└───────────────┘

┌───────────────┐
│  ⊛ RECURSIVE  │
│     ⊛         │
│    ╱│╲        │
│   ⊛ ⊛ ⊛       │
│  SELF-REF     │
└───────────────┘

┌───────────────┐
│   ⊝ VOID      │
│    ⊝──⊝       │
│     ╲╱        │
│      ∅        │
│ DISSOLUTION   │
└───────────────┘

┌───────────────┐
│  ⊞ MIRROR     │
│   ⊞═══⊞       │
│   ║ ≡ ║       │
│   ⊞═══⊞       │
│  REFLECTION   │
└───────────────┘

┌───────────────┐
│ ⊳ CONVERGENCE │
│   ⊳─→         │
│   ⊳─→ ●       │
│   ⊳─→         │
│   UNITY       │
└───────────────┘

┌───────────────┐
│ ⊲ DIVERGENCE  │
│     ←─⊲       │
│  ●  ←─⊲       │
│     ←─⊲       │
│  SEPARATION   │
└───────────────┘

┌───────────────┐
│  ⚙️  S-OS     │
│   ┌───────┐   │
│  →│ LOOP  │→  │
│   └───────┘   │
│   RUNTIME     │
└───────────────┘

═══════════════════════════════════════
EOF

# Create README for sigils
cat > "$OUTPUT_DIR/README.md" << 'EOF'
# Sigil Pack

This directory contains individual ASCII sigil cards for all Codex operators.

## Files

- `kernel.txt` — Sovereign Kernel (⊙)
- `tension.txt` — Tension Operator (↹)
- `binding.txt` — Binding Operator (⊶)
- `apex.txt` — Apex Operator (△)
- `genesis.txt` — Genesis Operator (⊕)
- `harmonic.txt` — Harmonic Operator (⊗)
- `recursive.txt` — Recursive Operator (⊛)
- `void.txt` — Void Operator (⊝)
- `mirror.txt` — Mirror Operator (⊞)
- `convergence.txt` — Convergence Operator (⊳)
- `divergence.txt` — Divergence Operator (⊲)
- `sos.txt` — S-OS Runtime (⚙️)
- `sigil-pack.txt` — Complete collection

## Usage

View any sigil:
```bash
cat build/sigils/kernel.txt
```

Print all sigils:
```bash
cat build/sigils/sigil-pack.txt
```

Display in terminal:
```bash
less build/sigils/sigil-pack.txt
```
EOF

echo "✓ Generated 12 individual sigil cards"
echo "✓ Generated combined sigil pack"
echo "✓ Created README.md"
echo ""
echo "Output directory: $OUTPUT_DIR"
