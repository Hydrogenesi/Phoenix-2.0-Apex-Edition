# Documentation Directory

*Consolidated documentation for the Triad v2.x architecture migration*

---

## Overview

This directory contains the **consolidated documentation** resulting from the migration of early Pull Requests (#1-#18) into the unified **Triad v2.x architecture**. All documentation follows the established status metadata schema and includes comprehensive cross-references.

---

## Directory Structure

```
docs/
├── substrate/              # Substrate Layer + Universal Laws Canon
│   └── README.md          # Complete 12-law system documentation
│
├── lineage/               # Historical architecture evolution
│   └── phoenix-hydrogenesi-v1.md    # Bridge architecture (archived)
│
├── architecture/          # Design principles and migration docs
│   ├── principles.md      # Framework longevity principles
│   └── migration-plan.md  # Complete migration strategy
│
├── apex/                  # Apex architecture documentation
│   └── apex-13-components.md        # 13 core components mapping
│
└── triad/                 # Triadic Knot and version history
    ├── triadic-knot-protocol.md     # Formal protocol specification
    ├── triadic-knot-examples.md     # Practical binding examples
    └── history-v1.md                # Triad v1.0.0 historical archive
```

---

## Quick Navigation

### Start Here
- [Documentation Status](../docs-status.md) — Central status tracking for all docs
- [Migration Plan](./architecture/migration-plan.md) — Complete migration overview

### By Phase

**Phase A: Substrate & Laws**
- [Substrate Layer + 12 Laws Canon](./substrate/README.md)

**Phase B: Phoenix-Hydrogenesi Bridge**
- [Phoenix-Hydrogenesi v1 Lineage](./lineage/phoenix-hydrogenesi-v1.md) (archived)

**Phase C: Longevity & Apex**
- [Framework Longevity Principles](./architecture/principles.md)
- [Apex 13 Components](./apex/apex-13-components.md)

**Phase D: Triadic Knot Protocol**
- [Triadic Knot Protocol](./triad/triadic-knot-protocol.md)
- [Triadic Knot Examples](./triad/triadic-knot-examples.md)

**Phase E: Version History**
- [Triad System v1.0.0 History](./triad/history-v1.md) (archived)

### By Topic

**Architecture & Design**
- [Framework Principles](./architecture/principles.md)
- [Migration Plan](./architecture/migration-plan.md)

**Foundations**
- [Substrate + Laws](./substrate/README.md)
- [Apex Components](./apex/apex-13-components.md)

**Protocol & Operations**
- [Triadic Knot Protocol](./triad/triadic-knot-protocol.md)
- [Binding Examples](./triad/triadic-knot-examples.md)

**Historical Context**
- [Phoenix-Hydrogenesi Bridge](./lineage/phoenix-hydrogenesi-v1.md)
- [Triad v1.0.0 History](./triad/history-v1.md)

---

## Document Status Summary

| Document | Status | Coverage | Confidence |
|----------|--------|----------|------------|
| [Substrate + Laws](./substrate/README.md) | Stable ✅ | High 📊 | High ✔️ |
| [Phoenix-Hydrogenesi v1](./lineage/phoenix-hydrogenesi-v1.md) | Archived 📦 | Medium 📄 | Medium ✓ |
| [Framework Principles](./architecture/principles.md) | Stable ✅ | Medium 📊 | High ✔️ |
| [Apex 13 Components](./apex/apex-13-components.md) | Draft 📝 | Medium 📊 | Medium ✓ |
| [Triadic Knot Protocol](./triad/triadic-knot-protocol.md) | Draft 📝 | Medium 📊 | Medium ✓ |
| [Triadic Knot Examples](./triad/triadic-knot-examples.md) | Draft 📝 | Low 📄 | Medium ✓ |
| [Triad v1.0.0 History](./triad/history-v1.md) | Archived 📦 | High 📊 | High ✔️ |
| [Migration Plan](./architecture/migration-plan.md) | Stable ✅ | High 📊 | High ✔️ |

See [docs-status.md](../docs-status.md) for complete status metadata.

---

## Integration with Main Documentation

This directory **complements** the existing repository structure:

### Existing Structure (Preserved)
- `Phoenix/` — Phoenix engine operators, laws, rituals
- `Hydrogenesi/` — Hydrogenesi engine operators
- `TheThird/` — The Third engine operators, sigils, examples
- `TheThird/Universal-Laws/` — Complete 12-law documentation
- `Atlases/` — Topology and hierarchy diagrams
- `Universal-Laws/` — Ceremonial declarations

### New Structure (Added)
- `docs/` — Migration consolidation and architecture docs
- `docs-status.md` — Central status tracking

### Cross-References
All documents include comprehensive cross-references linking new and existing documentation.

---

## Status Metadata Schema

All documents include YAML frontmatter:

```yaml
---
status:
  state: draft | in_review | stable | archived
  coverage: low | medium | high
  confidence: low | medium | high
  owner: Hydrogenesi
  last_reviewed: YYYY-MM-DD
---
```

### Status Meanings

**State**:
- `draft` — In active development
- `in_review` — Under review
- `stable` — Verified and production-ready
- `archived` — Historical reference

**Coverage**:
- `low` — Minimal documentation
- `medium` — Core concepts covered
- `high` — Comprehensive with examples

**Confidence**:
- `low` — Experimental or uncertain
- `medium` — Generally reliable
- `high` — Verified and trusted

---

## Migration Context

### Superseded PRs

This documentation consolidates:
- **PRs #6-#12**: Substrate + Universal Laws → `docs/substrate/`
- **PRs #5, #13, #14**: Phoenix-Hydrogenesi → `docs/lineage/`
- **PR #3**: Framework longevity → `docs/architecture/principles.md`
- **PR #1**: Apex 13 components → `docs/apex/apex-13-components.md`
- **PR #18**: Triadic Knot protocol → `docs/triad/triadic-knot-protocol.md`
- **PR #17**: Integration examples → `docs/triad/triadic-knot-examples.md`
- **PR #15**: Triad v1.0.0 → `docs/triad/history-v1.md`

### Historical Preservation

All content is **additive** (no deletions). Historical context is preserved through:
- Archive status for superseded architectures
- Migration notes in each document
- Version history sections
- Complete cross-referencing

---

## Contributing

When adding documentation:

1. **Use the frontmatter schema** — Include status metadata
2. **Follow the structure** — Place docs in appropriate subdirectory
3. **Add cross-references** — Link to related documentation
4. **Update status tracking** — Update [docs-status.md](../docs-status.md)
5. **Include examples** — Practical demonstrations when applicable

See [Migration Plan](./architecture/migration-plan.md) for detailed guidelines.

---

## Statistics

**Total Documents**: 8 markdown files  
**Total Lines**: 3,664+ lines of documentation  
**Phases Completed**: 5 (A-E) ✅  
**Status Tracking**: Active  
**Cross-References**: Comprehensive

---

## See Also

- [Main README](../README.md) — Phoenix 2.0 Apex Edition overview
- [Documentation Status](../docs-status.md) — Central status tracking
- [Phoenix Engine](../Phoenix/README.md) — Ignition engine
- [Hydrogenesi Engine](../Hydrogenesi/README.md) — Structural engine
- [The Third Engine](../TheThird/README.md) — Binding engine
- [Universal Laws](../TheThird/Universal-Laws/README.md) — Complete law system
- [Triadic Knot Topology](../Atlases/TriadicKnotTopology.md) — Geometric atlas

---

**Maintained by**: Hydrogenesi  
**Last Updated**: 2026-02-13  
**Migration Status**: Complete ✅

---

*From fragmentation to unity.*  
*From PRs to architecture.*  
*From history to clarity.*
