# Style Guide (Publication Mode)

This guide standardizes all Phoenix 2.0 Apex Edition documentation.

## 1) Terminology and Naming Rules

1. Always capitalize formal framework components: `Phoenix`, `Hydrogenesi`, `The Third`.
2. Use `Apex` (capitalized) for the convergence point as a concept.
3. Use `apex` (lowercase) only for generic prose.
4. Use `Three-Pillar System` for the architectural triad.
5. Use `Universal Laws` for the canonical law group.
6. Use `operators` for generic mentions, `Operators Atlas` for Book 05 references.
7. Refer to `Dragon Node` (not `DragonNode`).
8. Refer to `QPE` as `Quantum Pattern Engine (QPE)` on first mention.
9. Refer to `Phoenix Engine` on first mention, `Phoenix` afterward when unambiguous.
10. Keep operator symbols adjacent to names on first mention (example: `Genesis Operator (⊕)`).
11. Use `Codex` for the complete documentation corpus.
12. Use `book`, `chapter`, and `section` in lowercase unless part of a title.
13. Use `Book 09` formatting for numbered books.
14. Use two-digit chapter numbers in labels (`Chapter 01`).
15. Avoid introducing alternate names unless mapped in `TERMINOLOGY.md`.

## 2) Voice and Tone

16. Use instructional, direct voice.
17. Prefer short sentences for operational steps.
18. Use present tense for behavior and definitions.
19. Use imperative mood for procedures (`Run`, `Verify`, `Record`).
20. Avoid ambiguous pronouns when technical meaning can shift.
21. Keep ceremonial language consistent with procedural clarity.
22. Do not overstate certainty; indicate assumptions explicitly.
23. Use inclusive wording (`practitioners`, `readers`, `operators`).
24. Keep metaphoric language adjacent to concrete interpretation.
25. Use concise summaries at the top of long sections.

## 3) Markdown Structure

26. One H1 per file.
27. Use H2 for major sections, H3 for subtopics, H4 for implementation detail.
28. Keep heading text under 70 characters where possible.
29. Insert a blank line before and after tables.
30. Insert a blank line before and after fenced code blocks.
31. Use `-` bullet lists for unordered sets.
32. Use ordered lists for procedures and sequences.
33. Keep list item punctuation consistent within the same list.
34. Use definition callouts for term introduction.
35. Use horizontal rules (`---`) to separate major sections only.

## 4) Code Example Conventions

36. Always provide a language tag in code fences.
37. Keep examples runnable where possible.
38. Include expected output for non-trivial examples.
39. Avoid ellipses in executable examples unless clearly marked placeholder.
40. Use snake_case for Python variables.
41. Prefer explicit imports over wildcard imports.
42. Keep example dependencies minimal and documented.
43. Place safety checks in examples touching stateful systems.
44. Label pseudocode blocks explicitly as `text`.
45. For shell examples, include command prompts only when instructive.

## 5) Link Formatting and References

46. Use relative links inside `docs/`.
47. Prefer descriptive link text (`Engine Standards`) over `click here`.
48. Ensure link labels are action-oriented for navigation (`Open`, `Review`, `Compare`).
49. Keep one canonical target per concept when possible.
50. Add `See also` sections for dense technical pages.
51. Validate links after editing navigation structures.
52. Use anchor links for long page subsections.
53. Keep breadcrumb format consistent: `HOME > SECTION > PAGE`.
54. Use title case for nav-visible links.
55. Avoid raw URLs unless external.

## 6) Symbols, Operators, and Mathematical Notation

56. Use inline code for operator symbols in prose (`⊕`, `⊗`, `△`).
57. Use LaTeX blocks for multi-line equations.
58. Use consistent variable notation across chapters.
59. Define every variable before first equation use.
60. Use Unicode symbols consistently; avoid mixed ASCII substitutes.
61. Reserve `X` for Apex-state notation when discussing convergence.
62. Use `K_n` style for recursive state indexing.
63. Use `lim_{n\to\infty}` notation for convergence statements.
64. Keep inequality directions explicit and consistent.
65. Add a one-line interpretation under dense equations.

## 7) Editorial and Publication Quality

66. Remove filler adverbs (`very`, `simply`, `clearly`) unless necessary.
67. Replace vague adjectives with measurable descriptors.
68. Keep paragraph length to 3-6 lines in source markdown where practical.
69. Use callouts for warnings, definitions, and key insights.
70. Date-stamp significant page revisions in footer metadata.
71. Keep cross-book terminology synchronized with `TERMINOLOGY.md`.
72. Prefer stable references to conceptual definitions over repeating long explanations.
73. Avoid contradictory definitions across pages.
74. Favor diagrams for structure-heavy explanations.
75. Re-run publication checks before release.
