# Diagram Embedding Standards

## Reference Syntax

- ASCII embed: link to `docs/diagrams/<category>/<file>.md` and include fenced text block.
- Image embed: `![Alt text](relative/path.svg)`.
- Always include diagram ID and caption.

## Caption Format

`Diagram <ID> — <Short description>.`

## Alt-Text Rules

1. Describe the structure, not only appearance.
2. Include operator/cycle names.
3. Mention directional flow when present.

## Responsive Sizing

- Prefer SVG for vector diagrams.
- Keep default width <= 900 px.
- Avoid fixed heights unless required.

## Cross-References

- Add a `Related chapters` line below each diagram.
- Link to `DIAGRAM_INDEX.md` from every diagram-heavy page.
