# Documentation Status Metadata

## Overview

This document provides centralized status tracking for all documentation in the Phoenix 2.0 Apex Edition repository. Each document includes status metadata in its frontmatter following the schema defined below.

## Status Schema

Each document should include the following frontmatter:

```yaml
---
status:
  state: <state>         # draft | in_review | stable | archived
  coverage: <coverage>   # low | medium | high
  confidence: <confidence>  # low | medium | high
  owner: <owner>         # Document maintainer/owner
  last_reviewed: <date>  # YYYY-MM-DD format
---
```

### Field Definitions

#### state
The current lifecycle state of the document:
- **draft**: Document is under active development, content may be incomplete
- **in_review**: Document is complete but awaiting review
- **stable**: Document is reviewed, complete, and ready for use
- **archived**: Document represents historical content, superseded by newer versions

#### coverage
Assessment of how comprehensively the document covers its topic:
- **low**: Covers basic concepts only, significant gaps exist
- **medium**: Covers main concepts, some advanced topics may be missing
- **high**: Comprehensive coverage of all relevant aspects

#### confidence
Confidence in the accuracy and correctness of the content:
- **low**: Content is exploratory, may contain errors or uncertainties
- **medium**: Content is generally accurate, minor uncertainties may exist
- **high**: Content is verified, tested, and highly accurate

#### owner
The individual or team responsible for maintaining the document.

#### last_reviewed
Date when the document was last reviewed for accuracy and completeness (YYYY-MM-DD format).

## Documentation Status Table

### Core Architecture Documentation

| Doc Area | Path | State | Coverage | Confidence | Owner | Last Reviewed |
|----------|------|-------|----------|------------|-------|---------------|
| **Substrate + Universal Laws** | `docs/substrate/README.md` | stable | high | high | Hydrogenesi | 2026-02-13 |
| **Phoenix–Hydrogenesi v1 Lineage** | `docs/lineage/phoenix-hydrogenesi-v1.md` | archived | medium | medium | Hydrogenesi | 2026-02-13 |
| **Framework Longevity Principles** | `docs/architecture/principles.md` | stable | medium | high | Hydrogenesi | 2026-02-13 |
| **Apex 13 Components** | `docs/apex/apex-13-components.md` | draft | medium | medium | Hydrogenesi | 2026-02-13 |
| **Triadic Knot Protocol** | `docs/triad/triadic-knot-protocol.md` | draft | medium | medium | Hydrogenesi | 2026-02-13 |
| **Triadic Knot Binding Examples** | `docs/triad/triadic-knot-examples.md` | draft | low | medium | Hydrogenesi | 2026-02-13 |
| **Triad System v1.0.0 History** | `docs/triad/history-v1.md` | archived | high | high | Hydrogenesi | 2026-02-13 |

### Engine Documentation

| Doc Area | Path | State | Coverage | Confidence | Owner | Last Reviewed |
|----------|------|-------|----------|------------|-------|---------------|
| **Phoenix Engine** | `Phoenix/README.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Phoenix Operators** | `Phoenix/operators/*.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Phoenix Laws** | `Phoenix/laws/*.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Hydrogenesi Engine** | `Hydrogenesi/README.md` | stable | medium | high | Hydrogenesi | [Existing] |
| **Hydrogenesi Operators** | `Hydrogenesi/operators/README.md` | draft | low | medium | Hydrogenesi | [Existing] |
| **The Third Engine** | `TheThird/README.md` | stable | high | high | Hydrogenesi | [Existing] |
| **The Third Operators** | `TheThird/Operators/*.md` | stable | high | high | Hydrogenesi | [Existing] |

### Universal Laws

| Doc Area | Path | State | Coverage | Confidence | Owner | Last Reviewed |
|----------|------|-------|----------|------------|-------|---------------|
| **Universal Laws Overview** | `TheThird/Universal-Laws/README.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Substrate Laws** | `TheThird/Universal-Laws/substrate/*.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Universal Layer Laws** | `TheThird/Universal-Laws/universal/*.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Apex Layer Laws** | `TheThird/Universal-Laws/apex/*.md` | stable | high | high | Hydrogenesi | [Existing] |

### Topology and Reference

| Doc Area | Path | State | Coverage | Confidence | Owner | Last Reviewed |
|----------|------|-------|----------|------------|-------|---------------|
| **Triadic Knot Topology** | `Atlases/TriadicKnotTopology.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Codex Hierarchy Diagram** | `Atlases/CodexHierarchyDiagram.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Triadic Knot Sigils** | `TheThird/Sigils/*.md` | stable | high | high | Hydrogenesi | [Existing] |

### Examples and Guides

| Doc Area | Path | State | Coverage | Confidence | Owner | Last Reviewed |
|----------|------|-------|----------|------------|-------|---------------|
| **Phoenix-to-Knot Examples** | `TheThird/Examples/phoenix-to-knot.md` | stable | medium | high | Hydrogenesi | [Existing] |
| **Hydrogenesi-to-Knot Examples** | `TheThird/Examples/hydrogenesi-to-knot.md` | stable | medium | high | Hydrogenesi | [Existing] |
| **Triadic Loop Examples** | `TheThird/Examples/triadic-loop.md` | stable | medium | high | Hydrogenesi | [Existing] |
| **Apex Convergence Examples** | `TheThird/Examples/apex-convergence.md` | stable | medium | high | Hydrogenesi | [Existing] |
| **Quickstart Guide** | `Phoenix/guides/quickstart.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Glossary** | `Phoenix/guides/glossary.md` | stable | high | high | Hydrogenesi | [Existing] |

### Ceremonial and Canon

| Doc Area | Path | State | Coverage | Confidence | Owner | Last Reviewed |
|----------|------|-------|----------|------------|-------|---------------|
| **Phoenix Rituals** | `Phoenix/rituals/*.md` | stable | medium | high | Hydrogenesi | [Existing] |
| **Triad Canon** | `Universal-Laws/TriadCanon.md` | stable | high | high | Hydrogenesi | [Existing] |
| **Universal Laws Canon** | `Universal-Laws/README.md` | stable | high | high | Hydrogenesi | [Existing] |

## Status Transitions

### Draft → In Review
**Criteria**:
- Content complete for all planned sections
- All code examples tested (if applicable)
- Internal links verified
- Initial spell/grammar check complete

**Process**: Author requests review from owner/maintainer

### In Review → Stable
**Criteria**:
- Technical review completed
- Accuracy verified
- Cross-references checked
- Examples validated
- Approved by owner/maintainer

**Process**: Reviewer approves, owner updates status

### Stable → Archived
**Criteria**:
- Content superseded by newer documentation
- Historical reference value maintained
- Clear indicators of archived status
- Links to replacement documentation

**Process**: Owner decision, usually with new version release

### Archived → (No further transitions)
Archived documents remain archived. New documents are created for new versions.

## Review Schedule

### Regular Reviews
- **Stable documents**: Review annually or when architecture changes
- **Draft documents**: Review monthly until stable
- **Archived documents**: No regular review required

### Triggered Reviews
Reviews should be triggered by:
- Major architecture changes
- New version releases
- User feedback indicating inaccuracies
- Addition of new related documentation

## Maintenance Guidelines

### When to Update Status
Update the `last_reviewed` date when:
- Content is reviewed for accuracy
- Technical details are verified
- Examples are re-tested
- Links are checked

Update the `state` when:
- Document transitions through lifecycle
- Content completeness changes significantly
- Document is superseded

### Coverage Assessment
Assess coverage by considering:
- Are all major topics covered?
- Are edge cases documented?
- Are advanced topics included?
- Is the depth appropriate for the audience?

### Confidence Assessment
Assess confidence by considering:
- Has content been tested/verified?
- Are there known uncertainties?
- Has content been reviewed by experts?
- How mature is the underlying implementation?

## Migration from Early PRs

The following table maps early PRs to their consolidated documentation in Triad v2.x:

| Early PR | Topic | Consolidated Into | Status |
|----------|-------|-------------------|--------|
| #6–#12 | Substrate + Universal Laws + Sigils | `docs/substrate/README.md` + existing law docs | stable |
| #5, #13, #14 | Phoenix–Hydrogenesi unified architecture | `docs/lineage/phoenix-hydrogenesi-v1.md` | archived |
| #3 | Framework longevity | `docs/architecture/principles.md` | stable |
| #1 | Apex 13 components | `docs/apex/apex-13-components.md` | draft |
| #18 | Triadic Knot protocol | `docs/triad/triadic-knot-protocol.md` | draft |
| #17 | Integration examples | `docs/triad/triadic-knot-examples.md` | draft |
| #15 | Triad System v1.0.0 | `docs/triad/history-v1.md` | archived |

## Quick Reference

### Adding Status to New Documents

When creating a new document, add this frontmatter at the top:

```yaml
---
status:
  state: draft
  coverage: low
  confidence: low
  owner: YourName
  last_reviewed: YYYY-MM-DD
---
```

Then update the table in this document (`docs-status.md`) with the new entry.

### Checking Document Status

To see a document's status:
1. Check the frontmatter at the top of the document
2. Refer to this `docs-status.md` file for the centralized view

### Requesting Status Update

To request a status update for a document:
1. Review the document content
2. Verify technical accuracy
3. Update frontmatter with new status and review date
4. Update this central table
5. Commit changes with descriptive message

## Tools and Automation

### Future Enhancements
- Automated status extraction from frontmatter
- Status dashboard generation
- Automated link checking
- Coverage analysis tools
- Review reminder automation

### Current Process
Manual tracking via:
- Frontmatter in each document
- Central table in this document
- Git commit messages for change tracking

---

**Document Status**: This document itself is stable  
**Owner**: Hydrogenesi  
**Last Updated**: 2026-02-13
