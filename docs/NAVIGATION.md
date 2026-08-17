# Navigation Pattern Standards

## Core Rules

1. Use action-oriented link text (`Open`, `Review`, `Compare`).
2. Keep breadcrumb pattern: `HOME > SECTION > PAGE`.
3. Use `See Also` for concept-adjacent links.
4. Use `Related` for sibling references in same layer.
5. Use `Next` for sequential reading paths.
6. Place quick-reference terms near the top of chapter pages.
7. Keep TOC nesting to four levels maximum.
8. Ensure previous/next links are reciprocal when sequence exists.
9. Use parent-book links from every chapter-level page.
10. Use consistent chapter labels (`Book NN`, `Chapter NN`).
11. Use relative links for all in-repo navigation.
12. Keep external links explicit and isolated.
13. Add footer back-links to section roots.
14. Add at least one cross-book reference for integrative topics.
15. Add search keywords to major hub pages.
16. Keep duplicate links on a page minimal.

## Breadcrumb Patterns

- Chapters: `HOME > CODEX > [BOOK] > [CHAPTER]`
- Sections: `HOME > [SECTION] > [SUBSECTION]`
- Engine docs: `HOME > ENGINES > [ENGINE]`
- Ceremony docs: `HOME > CEREMONIES > [TYPE] > [CEREMONY]`

## Navigation Blocks

Use this block for chapter-like pages:

```markdown
## Navigation
- Previous: [Chapter N](...)
- Next: [Chapter N+1](...)
- Parent Book: [Book NN](...)
- Related: [Cross-book topic](...)
```
