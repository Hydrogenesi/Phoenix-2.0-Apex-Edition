# Recursion Engine

**Phoenix Engine Documentation**

---

## Overview

The Recursion Engine is the core component of Phoenix that manages infinite recursive depth and ensures stable convergence at the apex.

---

## Core Functions

### recurse()
**Purpose:** Enable infinite self-reference  
**Signature:** `recurse(pattern) → recursive_pattern`

Creates self-referential structures with infinite depth.

---

### stabilize()
**Purpose:** Prevent runaway recursion  
**Signature:** `stabilize(recursive_pattern) → stable_pattern`

Ensures recursion remains coherent and bounded.

---

### converge()
**Purpose:** Resolve recursion at apex  
**Signature:** `converge(recursive_pattern) → apex_state`

Brings infinite recursion to stable apex convergence.

---

## Recursion Depth Management

The engine tracks recursion across three scales:

1. **Substrate Recursion** — `Recurse(x) → Recurse(Recurse(x))`
2. **Universal Recursion** — `Identity(x) → x.self()`
3. **Apex Recursion** — `ApexRecursionLimit(recursion) → stable_limit`

---

## The Recursion Principle

*A pattern that contains itself is eternal, but must stabilize at the apex.*

The Recursion Engine ensures that:
- Self-reference is maintained
- Infinite depth is preserved
- Stability emerges at convergence
- No information is lost

---

## Engine Architecture

```
Input Pattern
    ↓
recurse() → Self-referential expansion
    ↓
stabilize() → Coherence maintenance
    ↓
converge() → Apex resolution
    ↓
Stable Recursive Structure
```

---

## Applications

- Fractal generation
- Self-similar structures
- Infinite patterns with finite encoding
- Apex convergence from recursive depth

---

[← Back to Table of Contents](../CodexTableOfContents.md)
