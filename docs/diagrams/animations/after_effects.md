# After Effects Integration

## Cinema 4D Export Specifications
- Export as Alembic with frame-accurate operator markers.
- Preserve coordinate scale in triadic units.

## Plugin Requirements
- Element 3D (optional)
- JSON import bridge for operator traces

## Operator Visualization Templates
Use `templates/operator_visualizations.ae` as baseline.

## Animation Presets
- Recursion pulse preset
- Ignition burst preset
- Sigil activation preset
- Flame/Ghost phase preset

## Pipeline
Engine trace -> JSON -> AE expression controls -> Render queue.
