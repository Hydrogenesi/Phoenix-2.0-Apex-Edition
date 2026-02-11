# SVG Assets

## Vector Graphics for Phoenix 2.0 Apex Edition

---

## Overview

This directory contains vector graphics (SVG format) for the Phoenix-Hydrogenesi framework, including:

- **Sigils** - Symbolic representations of operators and laws
- **Diagrams** - Architectural and flow visualizations
- **Icons** - UI elements and reference graphics

SVG format provides:
- **Scalability** - Crisp rendering at any size
- **Editability** - Modify with vector graphics tools
- **Web compatibility** - Direct embedding in HTML
- **Print quality** - High-resolution output

---

## Directory Structure

```
assets/svg/
├── README.md           (this file)
├── sigils/             Operator and law sigils
│   ├── conservation.svg
│   ├── symmetry.svg
│   ├── recursion.svg
│   ├── emergence.svg
│   ├── duality.svg
│   ├── recursive-identity.svg
│   ├── harmonic-resonance.svg
│   ├── tri-column-balance.svg
│   ├── phoenix-engine.svg
│   ├── hydrogenesi-engine.svg
│   └── triad-master.svg
└── diagrams/           System diagrams
    ├── codex-hierarchy.svg
    ├── operator-flow.svg
    ├── three-tier-architecture.svg
    └── triad-morphology.svg
```

---

## Sigil Specifications

### Design Principles

1. **Monochromatic Base** - Black lines on transparent background
2. **Consistent Stroke Width** - 2px for primary lines, 1px for details
3. **Geometric Precision** - Aligned to grid for clean rendering
4. **Scalable Details** - Legible from 16px to 1024px
5. **ASCII Correlation** - Visual similarity to text-based sigils

### Color Variants

Each sigil can be rendered in framework colors:

- **Phoenix Red**: `#B40000` (RGB 180, 0, 0)
- **Hydrogenesi Blue**: `#003C78` (RGB 0, 60, 120)
- **Apex Gold**: `#B8860B` (RGB 184, 134, 11)
- **Substrate Purple**: `#4B0082` (RGB 75, 0, 130)

---

## Generating SVGs

### From ASCII Art

```bash
# Use the export script
cd assets/scripts
./export-svg.sh

# Or manually with a converter
ascii-to-svg input.txt output.svg --font "Fira Code" --size 16
```

### From Vector Editor

Recommended tools:
- **Inkscape** (free, open source)
- **Adobe Illustrator** (professional)
- **Figma** (web-based, collaborative)

Guidelines:
1. Create on 512×512px canvas
2. Center artwork
3. Use paths, not text (convert text to paths)
4. Save as "Plain SVG" (not Inkscape SVG)
5. Optimize with SVGO

---

## Optimization

### SVGO (SVG Optimizer)

Install:
```bash
npm install -g svgo
```

Optimize all SVGs:
```bash
cd assets/svg
svgo sigils/*.svg --multipass --pretty
svgo diagrams/*.svg --multipass --pretty
```

Benefits:
- Smaller file size (30-50% reduction typical)
- Cleaner markup
- Better rendering performance

---

## Usage Examples

### HTML Embedding

#### Inline SVG
```html
<svg width="64" height="64" viewBox="0 0 512 512">
  <!-- SVG content -->
</svg>
```

#### Image Tag
```html
<img src="assets/svg/sigils/recursion.svg" 
     alt="Recursive Operator" 
     width="64" height="64">
```

#### CSS Background
```css
.operator-recursive {
  background-image: url('assets/svg/sigils/recursion.svg');
  background-size: contain;
  width: 64px;
  height: 64px;
}
```

---

### Markdown Embedding

```markdown
![Recursive Operator](assets/svg/sigils/recursion.svg)
```

---

### LaTeX Integration

Via Inkscape:
```bash
inkscape recursion.svg --export-pdf=recursion.pdf
```

In LaTeX:
```latex
\usepackage{graphicx}
\includegraphics[width=2cm]{recursion.pdf}
```

---

## Conversion to Other Formats

### To PNG (Raster)

```bash
# High-res (1024px)
inkscape recursion.svg --export-png=recursion.png --export-width=1024

# Multiple sizes
for size in 16 32 64 128 256 512 1024; do
  inkscape recursion.svg --export-png=recursion-${size}.png \
          --export-width=${size}
done
```

### To PDF

```bash
inkscape recursion.svg --export-pdf=recursion.pdf
```

### To EPS (for LaTeX)

```bash
inkscape recursion.svg --export-eps=recursion.eps
```

---

## Sigil Catalog

### Operator Sigils

| File | Operator | Symbol | Description |
|------|----------|--------|-------------|
| `genesis.svg` | Genesis | ⊕ | Creation from void |
| `harmonic.svg` | Harmonic | ⊗ | Resonance binding |
| `recursive.svg` | Recursive | ⊛ | Self-reference |
| `apex.svg` | Apex | △ | Triad formation |
| `void.svg` | Void | ⊝ | Nullification |
| `mirror.svg` | Mirror | ⊞ | Reflection |
| `convergence.svg` | Convergence | ⊳ | Unification |
| `divergence.svg` | Divergence | ⊲ | Separation |

### Law Sigils

| File | Law | Layer | Description |
|------|-----|-------|-------------|
| `conservation.svg` | Conservation | Substrate | Essence preservation |
| `symmetry.svg` | Symmetry | Substrate | Complementary reflection |
| `recursion.svg` | Recursion | Substrate | Self-replication |
| `emergence.svg` | Emergence | Substrate | Complex from simple |
| `duality.svg` | Duality | Substrate | Paired phenomena |
| `recursive-identity.svg` | Recursive Identity | Universal | Generation pattern |
| `harmonic-resonance.svg` | Harmonic Resonance | Universal | Phase alignment |
| `tri-column-balance.svg` | Tri-Column Balance | Universal | Three-component stability |

### System Diagrams

| File | Content | Purpose |
|------|---------|---------|
| `codex-hierarchy.svg` | Full documentation tree | Navigation reference |
| `operator-flow.svg` | Operator relationships | Understanding composition |
| `three-tier-architecture.svg` | Layer structure | System overview |
| `triad-morphology.svg` | Triad transformations | Formation patterns |
| `phoenix-engine.svg` | Phoenix architecture | Engine understanding |
| `hydrogenesi-engine.svg` | Hydrogenesi architecture | Engine understanding |

---

## Development Workflow

### Creating New Sigils

1. **Design in editor**
   - Start from template or ASCII reference
   - Follow design principles
   - Use consistent style

2. **Export**
   - Save as Plain SVG
   - Remove unnecessary metadata
   - Check file size (<10KB typical)

3. **Optimize**
   ```bash
   svgo new-sigil.svg --pretty
   ```

4. **Test**
   - View at multiple sizes
   - Check on dark/light backgrounds
   - Verify in target contexts (web, print, PDF)

5. **Document**
   - Add entry to this README
   - Update SIGIL_ATLAS.md if applicable
   - Cross-reference in related docs

---

## Color Palette

Official colors (define in SVG):

```svg
<defs>
  <style>
    .phoenix-red { fill: #B40000; }
    .hydrogenesi-blue { fill: #003C78; }
    .apex-gold { fill: #B8860B; }
    .substrate-purple { fill: #4B0082; }
    .neutral-black { fill: #000000; }
  </style>
</defs>
```

Usage:
```svg
<path class="phoenix-red" d="M..."/>
```

---

## Accessibility

Ensure SVGs are accessible:

```svg
<svg role="img" aria-labelledby="title desc">
  <title id="title">Recursive Operator</title>
  <desc id="desc">A triangular fractal pattern representing self-reference</desc>
  <!-- SVG content -->
</svg>
```

---

## License

All SVG assets are released under the same MIT License as the Phoenix 2.0 Apex Edition framework. See [LICENSE](../../LICENSE) for details.

---

## Tools and Resources

### Recommended Software

- **Inkscape** - https://inkscape.org/
- **SVGO** - https://github.com/svg/svgo
- **SVGOMG** - https://jakearchibald.github.io/svgomg/ (web UI)

### Learning Resources

- SVG Tutorial: https://developer.mozilla.org/en-US/docs/Web/SVG
- Inkscape Manual: https://inkscape.org/doc/
- SVG Optimization Guide: https://web.dev/svg-optimization/

### Inspiration

- Sacred Geometry patterns
- Alchemical symbols
- Mathematical diagrams
- Ceremonial sigils

---

## Future Enhancements

- Animated SVGs for web interface
- Interactive diagrams with JavaScript
- 3D renderings (SVG as base for projection)
- Font creation from sigils
- Procedural generation scripts

---

*"From vector paths emerges ceremony; from geometry, meaning."*
