# Documentation Status Metadata

*Tracking documentation states across the Triad v2.x architecture migration*

---

## Status Schema

Each documentation area tracks the following metadata fields:

- **status.state**: Current lifecycle state
  - `draft` — In active development
  - `in_review` — Under review for accuracy
  - `stable` — Verified and production-ready
  - `archived` — Historical reference, no longer active

- **status.coverage**: Documentation completeness
  - `low` — Minimal documentation, significant gaps
  - `medium` — Core concepts covered, details may be sparse
  - `high` — Comprehensive documentation with examples

- **status.confidence**: Accuracy and reliability
  - `low` — Experimental or uncertain content
  - `medium` — Generally reliable, may need verification
  - `high` — Verified and trusted

- **status.owner**: Primary maintainer or author
- **status.last_reviewed**: Date of last review (YYYY-MM-DD)

---

## Documentation Status Table

| Doc Area | Path / Anchor | Status.State | Status.Coverage | Status.Confidence | Status.Owner | Status.Last_Reviewed |
|----------|---------------|--------------|-----------------|-------------------|--------------|----------------------|
| Substrate + Universal Laws Canon | `docs/substrate/` | `stable` | `high` | `high` | `Hydrogenesi` | `2026-02-13` |
| Phoenix-Hydrogenesi v1 Lineage | `docs/lineage/phoenix-hydrogenesi-v1.md` | `archived` | `medium` | `medium` | `Hydrogenesi` | `2026-02-13` |
| Framework Longevity Principles | `docs/architecture/principles.md` | `stable` | `medium` | `high` | `Hydrogenesi` | `2026-02-13` |
| Apex 13 Components | `docs/apex/apex-13-components.md` | `draft` | `medium` | `medium` | `Hydrogenesi` | `2026-02-13` |
| Triadic Knot Protocol | `docs/triad/triadic-knot-protocol.md` | `draft` | `medium` | `medium` | `Hydrogenesi` | `2026-02-13` |
| Triadic Knot Binding Examples | `docs/triad/triadic-knot-examples.md` | `draft` | `low` | `medium` | `Hydrogenesi` | `2026-02-13` |
| Triad System v1.0.0 History | `docs/triad/history-v1.md` | `archived` | `high` | `high` | `Hydrogenesi` | `2026-02-13` |

---

## YAML Frontmatter Template

For individual documentation files, use this frontmatter:

```yaml
---
status:
  state: draft        # draft | in_review | stable | archived
  coverage: medium    # low | medium | high
  confidence: medium  # low | medium | high
  owner: Hydrogenesi
  last_reviewed: 2026-02-13
---
```

---

## Usage Guidelines

### Updating Status

When updating documentation:
1. Update the `last_reviewed` date to current date
2. Adjust `state`, `coverage`, and `confidence` as appropriate
3. Update both this central table and the file's frontmatter

### State Transitions

Typical lifecycle flow:
```
draft → in_review → stable
                      ↓
                  archived (when superseded)
```

### Coverage Progression

As documentation matures:
```
low → medium → high
```

Coverage increases as:
- Examples are added
- Edge cases are documented
- Cross-references are completed
- Integration guides are written

### Confidence Growth

Confidence increases through:
- Peer review
- Practical validation
- Time-tested stability
- Community feedback

---

## Migration Status

### Completed Phases
- ✅ Phase 0: Documentation infrastructure setup

### In Progress
- 🔄 Phase A: Substrate + Laws consolidation
- 🔄 Phase B: Phoenix-Hydrogenesi unified architecture
- 🔄 Phase C: Longevity + Apex Edition
- 🔄 Phase D: Triadic Knot protocol
- 🔄 Phase E: Triad System v1.0.0 archive

### Planned
- 📋 Phase F: Visual lineage diagram generation
- 📋 Phase G: Cross-reference validation
- 📋 Phase H: Final review and stabilization

---

## See Also

- [Migration Plan](./docs/architecture/migration-plan.md) — Complete migration strategy
- [Contributing Guidelines](./CONTRIBUTING.md) — Documentation standards
- [Phoenix 2.0 README](./README.md) — Main repository documentation

---

*Last Updated: 2026-02-13*  
*Maintained by: Hydrogenesi*
