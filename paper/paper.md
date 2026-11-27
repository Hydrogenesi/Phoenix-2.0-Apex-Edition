---
title: 'Cold Fold Engine: an executable codex for testing the Cold Fold cosmogenic framework against raw measurement, within Phoenix 2.0 Apex Edition'
tags:
  - Python
  - astrophysics
  - cosmogony
  - theory testing
  - verification
authors:
  - name: James Stanley
    orcid: 0000-0000-0000-0000   # [FILL] your ORCID iD (free at orcid.org) — JOSS strongly expects one
    affiliation: 1
affiliations:
  - name: Independent Researcher, United States   # [CONFIRM] city/state if you want it shown
    index: 1
date: 27 November 2026
bibliography: paper.bib
---

<!--
  DRAFT — notes for James (delete before submitting):
  * [FILL] = information only you have.  [CONFIRM] = I inferred it from the
    public cold-fold-framework repo; check it against the engine's real code.
  * Target length 750–1,750 words (JOSS limit). This draft is ~1,050.
  * JOSS reviews the SOFTWARE, not the theory. The paper must not present new
    physics results; it describes what the software does and who it is for.
  * Build a PDF preview locally with the Open Journals action (see .github/workflows/draft-pdf.yml).
-->

# Summary

The Cold Fold framework is a cosmogenic model that describes the
path from an origin event (the "cold fold" of infinity) through accretion,
ignition, and three structural domains — atomic, nuclear, and elliptical — to
stars, galaxies, and life. The framework is written as a codex: a set of
numbered sections, each stating a claim, its sequence of stages, a named
operator, a mechanism, the measurements it shares with the current paradigm,
and the tests that could separate the two.

The Cold Fold Engine is a Python package (`cold_fold`), developed inside the
Phoenix 2.0 Apex Edition repository alongside its stellar-structure and
operator modules, that turns the codex into executable form. Each codex operator (for example `COLD_FOLD()` and
`IGNITE_ACCRETION()`) is represented as an ordered state sequence, each
codex law (such as the Secretion Law, "no secretion, no accretion," and the
Current Law, "no current, no replication") is encoded as an invariant over
those sequences, and each codex section exposes a verification routine that
returns a structured, machine-readable result. A single command runs the
full verification suite and reports which sections are internally
consistent, which laws hold across every operator, and which items remain
open in the codex's Open Ledger. [CONFIRM: module names and the exact CLI
command — e.g. `cold-fold verify`.]

# Statement of need

Alternative theoretical frameworks in astrophysics are usually published as
prose, which makes them hard to check, hard to compare with the current
paradigm, and hard to falsify. Readers cannot easily tell whether a
framework's stages are mutually consistent, whether a stated law is actually
respected everywhere the framework uses it, or which raw measurement would
decide between the framework and the current paradigm.

The Cold Fold Engine addresses this for the Cold Fold framework. It is
intended for (a) researchers who want to examine the framework's internal
logic without reconstructing it by hand, (b) reviewers who need a precise,
versioned statement of what the framework claims, and (c) anyone who wants
to confront the framework's predictions with public data. Because every
codex claim is tied to the raw measurement it predicts — pulse timing,
photon counts, spectral lines, proper motions — rather than to a
model-derived label, the engine makes explicit where the Cold Fold
framework and the current paradigm predict different measurements, which
the codex treats as the decisive tests.

# State of the field

General-purpose astrophysics software such as Astropy [@astropy2022] and
stellar-evolution codes such as MESA [@paxton2011] implement the current
paradigm and are not designed to encode or check a competing framework.
Proof assistants and formal-methods tools can verify logical structure but
require expertise far beyond most readers of a physical theory, and they do
not connect claims to observational data. We are not aware of an existing
package that represents a cosmogenic framework as executable operators with
per-section consistency checks and an explicit link from each claim to a
raw-measurement test. Building this as a separate package, rather than
contributing to an existing project, was necessary because the framework's
vocabulary and stage structure are its own and do not map onto the data
models of current-paradigm codes.

# Software design

The central design choice is **one codex section, one verifiable unit**.
The codex already follows a fixed order — Statement, Sequence, Operator,
Mechanism, Shared Observations, Tests — so the engine mirrors that order in
code. Each section is a module that declares its stage sequence, its
operator, and its invariants, and each returns a result object with a
pass/fail status and a details dictionary. This keeps a one-to-one
correspondence between the written codex and the code: when the codex is
revised (for example, the Sister Split was rewritten from a multi-step
sequence into a single act), the corresponding module changes and its tests
show exactly what moved. [CONFIRM against the engine's real layout.]

A second choice is to **separate raw measurement from interpretation** in
the data model. Observations the codex cites are stored as the quantity an
instrument records, never by the current paradigm's label for it. This
follows the codex's Method section and lets the same measurement be read
through either framework without one being treated as the default.

Third, the engine favours **plain, dependency-light Python**: the core
needs only the standard library and NumPy [@harris2020], so the full
verification suite runs in seconds on a laptop and in continuous
integration on every commit. The engine shares the Phoenix repository's
test suite and continuous integration (Linux and Windows), and uses the
same convention for honest testing: checks against textbook physics are
marked, and documented defects are kept as strict expected failures that
turn into test failures once fixed, so the suite never hides a known
problem. The trade-off is that the engine does not yet
perform heavy numerical simulation; it prioritises transparency and
checkability of the framework's logic. [CONFIRM dependency list.]

# Research impact statement

[FILL — this section must be specific, not aspirational. JOSS asks for
either realised impact (others using it, citations, integrations) or
credible near-term significance (benchmarks, reproducible materials,
community readiness). Candidate evidence to build before submitting:]

- A reproducible comparison of a codex test with public data, for example
  the codex's pulsar-kick test (an asymmetric polar breach should leave a
  kick aligned with the breached pole) run against proper motions and
  spin-axis estimates from the ATNF Pulsar Catalogue [@manchester2005].
- The Phoenix repository has been developed in public since February 2026;
  cite its release history and test-suite growth here.
- Archived, versioned releases with a DOI (e.g. via Zenodo) so the exact
  codex version tested is citable.
- Any use of the engine by people other than the author.

The codex's other raw-measurement tests are natural next targets: paired,
simultaneous opposite ejections such as those of GRS 1915+105
[@mirabel1994]; the arrival-time difference between gravitational and
electromagnetic signals from GW170817 [@abbott2017]; and the joint
X-ray–radio bursts of SGR 1935+2154 [@bochenek2020].

# AI usage disclosure

[CONFIRM and complete — JOSS treats an incomplete disclosure as an ethics
issue.] Generative AI tools were used in this project. GitHub Copilot's coding agent
[FILL: period] authored a large share of the repository's commits (about
140 of roughly 250) under the author's direction; [FILL: describe what it
wrote and how you checked it]. Claude (Anthropic, Claude Opus 5.5) helped draft this paper,
the README, and the continuous-integration configuration. All of the
framework's concepts, laws and operators, along with the software's design
decisions, are the author's. The author reviewed, edited and validated all
AI-assisted text and code and ran the full test suite to confirm
correctness.

# Acknowledgements

[FILL or delete. State any financial support; if none, say "This work
received no external funding."]

# References
