# JOSS readiness: Cold Fold Engine in Phoenix 2.0 Apex Edition

Checked 27 November 2026 against the JOSS submission and paper guidelines.

| Requirement | Status | Notes |
|---|---|---|
| OSI license | ✅ | MIT, © 2026 James Stanley |
| **Public for 6+ months** | ✅ | Public since 3 Feb 2026 (almost 10 months) |
| Active development across that period | ⚠️ | 249 commits, but no commits in April or August 2026. Keep committing regularly from now on |
| Automated tests + CI | ✅ | 89 pass, 9 strict xfails; CI on Linux and Windows |
| Engine tests | ❌ | `cold_fold/` is not in the repo yet. Add it with tests in `tests/` |
| Documentation | ⚠️ | README now has an engine section; needs API docs and a worked example |
| paper.md + paper.bib | ✅ Drafted | `paper/`, with all required sections, ~1,050 words |
| Research impact | ❌ **Blocker** | Needs specific evidence. Best route: run the codex's §3 pulsar-kick test on the public ATNF Pulsar Catalogue inside the engine |
| AI disclosure | ⚠️ **Important** | Copilot's agent made about 142 of 249 commits. JOSS requires full disclosure and that the author is a major contributor. Describe what Copilot wrote and how you checked it |
| ORCID | ⚠️ | Add it to paper.md and CITATION.cff |

## Earliest submission

The age rule is already met. What's left: add the engine code and tests, build
one data-backed test (research impact), and complete the AI disclosure. Then
submit.

## Clean-up before submitting

- Remove the committed build outputs: `Phoenix-2.0-Apex-Edition-v2.0.0-apex.zip`
  (644 KB), `dist/` and `hydrogenesis.egg-info/`. Publish the zip as a GitHub
  Release instead, and add these paths to `.gitignore`.
- Fix the README badges: they render as `[!\[License…` because of stray
  backslashes.
- Correct any Copilot-written text that misstates your views before reviewers read it.
- Tag a release and connect Zenodo for a free DOI.
