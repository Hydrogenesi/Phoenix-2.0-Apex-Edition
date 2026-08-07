#!/usr/bin/env python3
"""
phoenix_ignition.py

Phoenix Ignition Engine — The Transformative Core of The Triad
Phoenix 2.0 Apex Edition

Implements:
- The Eight Phoenix Operators (⊕ ⊗ ⊛ △ ⊝ ⊞ ⊳ ⊲)
- The Five Substrate Laws (Conservation, Symmetry, Recursion, Emergence, Duality)
- Ritual sequence execution (ignite, cycle, converge)
- CLI ignition interface

Operator Notation:
    ⊕  Genesis     — Create from void
    ⊗  Harmonic    — Stabilize and amplify
    ⊛  Recursive   — Self-referential fold
    △  Apex        — Reach maximum coherence
    ⊝  Void        — Return to primordial state
    ⊞  Mirror      — Symmetric inversion
    ⊳  Convergence — Combine patterns into unity
    ⊲  Divergence  — Split pattern into components

Full Cycle:
    Phoenix (transform) → Hydrogenesi (preserve) → The Third (bind) → Apex (converge)

Version: 2.0.0
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional, Tuple


_hash_cache = {}
_HASH_CACHE_MAXSIZE = 4096


def fast_hash(state):
    key = repr(state)
    if key in _hash_cache:
        value = _hash_cache.pop(key)
        _hash_cache[key] = value
        return value
    if len(_hash_cache) >= _HASH_CACHE_MAXSIZE:
        _hash_cache.pop(next(iter(_hash_cache)))
    _hash_cache[key] = hashlib.sha1(key.encode()).hexdigest()[:8]
    return _hash_cache[key]


# --------------------------------------------------------
# 1. Pattern — the fundamental unit of Phoenix operations
# --------------------------------------------------------

@dataclass
class Pattern:
    """
    A harmonic pattern in the Phoenix transformation system.

    Attributes:
        id:     Unique pattern identifier (short hash by default).
        state:  The pattern's content or label.
        energy: Harmonic energy level (must be >= 0).
        depth:  Recursion depth (incremented by ⊛).
    """

    id: str
    state: Any
    energy: float = 1.0
    depth: int = 0

    def __post_init__(self) -> None:
        if not self.id:
            self.id = fast_hash(self.state)

    def __repr__(self) -> str:
        return f"Ψ[{self.id}](e={self.energy:.3f}, d={self.depth})"

    @classmethod
    def void(cls) -> "Pattern":
        """Return the void/null pattern ∅."""
        return cls(id="∅", state=None, energy=0.0, depth=0)

    def is_void(self) -> bool:
        """Return True if this pattern is the void state."""
        return self.state is None

    def complexity(self) -> float:
        """Compute a complexity measure used by the Apex operator."""
        if self.is_void():
            return 0.0
        return self.energy * (1 + math.log1p(self.depth))


# --------------------------------------------------------
# 2. The Five Substrate Laws
# --------------------------------------------------------

class LawViolation(Exception):
    """Raised when a Phoenix Substrate Law is violated."""


def law_conservation(_pattern_in: Pattern, pattern_out: Pattern) -> None:
    """
    Law of Conservation: energy must be accounted for across transformations.

    Raises LawViolation if the output pattern has negative energy.
    """
    if pattern_out.energy < 0:
        raise LawViolation(
            f"Conservation violated: output energy {pattern_out.energy:.6f} < 0"
        )


def law_symmetry(pattern: Pattern, mirror: Pattern) -> bool:
    """
    Law of Symmetry: every operator has a mirror form.

    Returns True if *pattern* and *mirror* carry equal energy (symmetric).
    """
    return abs(pattern.energy - mirror.energy) < 1e-6


def law_recursion(pattern: Pattern, max_depth: int = 64) -> None:
    """
    Law of Recursion: patterns repeat across scales until apex is reached.

    Raises LawViolation when recursion depth exceeds *max_depth*.
    Apply ⊗ (Harmonic) to stabilize before continuing deep recursion.
    """
    warning_depth = math.ceil(max_depth / 2)
    if warning_depth <= pattern.depth < max_depth:
        warnings.warn(
            f"Recursion depth {pattern.depth} reached warning threshold "
            f"({warning_depth}/{max_depth}). Consider applying ⊗ stabilization.",
            RuntimeWarning,
            stacklevel=2,
        )
    if pattern.depth > max_depth:
        raise LawViolation(
            f"Recursion depth {pattern.depth} exceeds maximum {max_depth}. "
            "Apply ⊗ (Harmonic) to stabilize before continuing."
        )


def law_emergence(patterns: List[Pattern], threshold: float = 2.0) -> bool:
    """
    Law of Emergence: complexity arises from simple rules.

    Returns True when the combined complexity of *patterns* meets *threshold*.
    """
    return sum(p.complexity() for p in patterns) >= threshold


def law_duality(pattern: Pattern) -> Tuple[Pattern, Pattern]:
    """
    Law of Duality: all states exist in superposition of form and void.

    Returns the pattern and its dual (void-partner) whose energies sum to 1.
    """
    dual_state = f"~{pattern.state}" if pattern.state is not None else None
    dual = Pattern(
        id=f"~{pattern.id}",
        state=dual_state,
        energy=max(0.0, 1.0 - pattern.energy),
        depth=pattern.depth,
    )
    return pattern, dual


# --------------------------------------------------------
# 3. The Eight Phoenix Operators
# --------------------------------------------------------

class PhoenixOperator(Enum):
    """The eight Phoenix transformation operators."""

    GENESIS = "⊕"
    HARMONIC = "⊗"
    RECURSIVE = "⊛"
    APEX = "△"
    VOID = "⊝"
    MIRROR = "⊞"
    CONVERGENCE = "⊳"
    DIVERGENCE = "⊲"


def op_genesis(state: Any = None, energy: float = 1.0) -> Pattern:
    """
    ⊕ Genesis Operator — Creation from void.

    ⊕(∅) → Ψ₀

    Transforms the void into the primordial pattern.  All operator sequences
    must begin with Genesis to establish the initial pattern state.
    """
    if state is None:
        label = "Ψ₀"
    else:
        label = str(state)
    pattern_id = fast_hash(label)
    result = Pattern(id=pattern_id, state=label, energy=energy, depth=0)
    law_conservation(Pattern.void(), result)
    return result


def op_harmonic(pattern: Pattern, amplify: float = 1.0) -> Pattern:
    """
    ⊗ Harmonic Operator — Stabilization and resonance.

    ⊗(Ψ) → Ψ′

    Amplifies and stabilizes an existing pattern.  Use *amplify* > 1 to boost
    energy; use *amplify* = 1 for a pure stabilization pass.
    """
    result = Pattern(
        id=f"{pattern.id}'",
        state=pattern.state,
        energy=pattern.energy * amplify,
        depth=pattern.depth,
    )
    law_conservation(pattern, result)
    return result


def op_recursive(pattern: Pattern) -> Pattern:
    """
    ⊛ Recursive Operator — Self-referential folding.

    ⊛(Ψ) → Ψ₊₁

    Folds a pattern back upon itself, incrementing depth.  Always follow
    with ⊗ (Harmonic) to prevent unstable accumulation.
    """
    result = Pattern(
        id=f"⊛{pattern.id}",
        state=f"⊛({pattern.state})",
        energy=pattern.energy,
        depth=pattern.depth + 1,
    )
    law_recursion(result)
    law_conservation(pattern, result)
    return result


def op_apex(pattern: Pattern, threshold: float = 2.0) -> Pattern:
    """
    △ Apex Operator — Culmination at maximum coherence.

    △(Ψₙ) → Apex

    Raises *pattern* to apex form once its complexity meets *threshold*.
    Use ⊛ and ⊗ in combination to build sufficient complexity first.

    Raises:
        LawViolation: if pattern complexity is below *threshold*.
    """
    if pattern.complexity() < threshold:
        raise LawViolation(
            f"Premature Apex: complexity {pattern.complexity():.3f} < "
            f"threshold {threshold}. "
            "Use ⊛ and ⊗ to build complexity first."
        )
    return Pattern(
        id="△",
        state="Apex",
        energy=pattern.energy,
        depth=pattern.depth,
    )


def op_void(pattern: Pattern) -> Pattern:
    """
    ⊝ Void Operator — Ceremonial dissolution to primordial state.

    ⊝(Ψ) → ∅

    Returns the pattern to void.  This is not a true reversal of Genesis but
    a ceremonial dissolution (the inverse path of creation).
    """
    return Pattern.void()


def op_mirror(pattern: Pattern) -> Pattern:
    """
    ⊞ Mirror Operator — Symmetric inversion.

    ⊞(Ψ) → Ψ*

    Creates a symmetric inversion of the pattern.  The mirror carries the
    same energy, satisfying the Law of Symmetry.
    """
    return Pattern(
        id=f"{pattern.id}*",
        state=f"⊞({pattern.state})",
        energy=pattern.energy,
        depth=pattern.depth,
    )


def op_convergence(*patterns: Pattern) -> Pattern:
    """
    ⊳ Convergence Operator — Integration into unity.

    ⊳(Ψ₁, Ψ₂, …) → Ψ_unified

    Combines two or more patterns into a single unified pattern whose energy
    is the sum of all inputs.

    Raises:
        ValueError: if fewer than two patterns are supplied.
    """
    if len(patterns) < 2:
        raise ValueError("Convergence requires at least two patterns.")

    combined_state = "⊳(" + ", ".join(str(p.state) for p in patterns) + ")"
    total_energy = sum(p.energy for p in patterns)
    max_depth = max(p.depth for p in patterns)
    unified_id = "⊳" + "".join(p.id[:4] for p in patterns)

    result = Pattern(
        id=unified_id,
        state=combined_state,
        energy=total_energy,
        depth=max_depth,
    )
    # Validate against total combined input energy rather than a single input pattern
    combined_in = Pattern(id="⊳in", state=None, energy=total_energy, depth=max_depth)
    law_conservation(combined_in, result)
    return result


def op_divergence(pattern: Pattern) -> Tuple[Pattern, Pattern]:
    """
    ⊲ Divergence Operator — Separation into two components.

    ⊲(Ψ) → (Ψ₁, Ψ₂)

    Splits a pattern into two equal-energy components.  Energy is conserved
    across the split (each component carries half the original energy).
    """
    half_energy = pattern.energy / 2.0
    left = Pattern(
        id=f"{pattern.id}₁",
        state=f"⊲₁({pattern.state})",
        energy=half_energy,
        depth=pattern.depth,
    )
    right = Pattern(
        id=f"{pattern.id}₂",
        state=f"⊲₂({pattern.state})",
        energy=half_energy,
        depth=pattern.depth,
    )
    return left, right


# --------------------------------------------------------
# 4. PhoenixIgnition — ritual sequence orchestrator
# --------------------------------------------------------

class PhoenixIgnition:
    """
    Phoenix Ignition Engine — orchestrates Phoenix ritual operator sequences.

    This is the primary interface for the Phoenix transformation system.
    Instantiate with ``verbose=True`` to print each operator step.

    Example::

        engine = PhoenixIgnition(verbose=True)
        apex = engine.ignite(seed="my-pattern")

    Ritual sequences available:

    - :meth:`ignite`   — Basic Phoenix sequence (⊕ → ⊗ → ⊛ → △)
    - :meth:`cycle`    — Phoenix Rebirth Cycle (⊕ → ⊗ → ⊝ → ⊕ → ⊗)
    - :meth:`converge` — Convergent Synthesis (⊕×N → ⊳ → ⊗ → ⊛ → △)
    """

    APEX_THRESHOLD = 2.0

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self._log: List[str | Callable[[], str]] = []

    def _emit(self, msg: str | Callable[[], str]) -> None:
        if callable(msg):
            if self.verbose:
                rendered = msg()
                self._log.append(rendered)
                print(rendered)
            else:
                self._log.append(msg)
            return
        self._log.append(msg)
        if self.verbose:
            print(msg)

    # ------------------------------------------------------------------
    # Ritual: Basic Phoenix Sequence
    # ⊕(∅) → Ψ₀  →  ⊗(Ψ₀) → Ψ₀′  →  ⊛(Ψ₀′) → Ψ₁  →  △(Ψ₁) → Apex
    # ------------------------------------------------------------------

    def ignite(self, seed: Optional[Any] = None) -> Pattern:
        """
        Execute the basic Phoenix ignition sequence.

        ⊕(∅) → ⊗ → ⊛ → ⊗ → △

        Args:
            seed: Optional value to seed the initial Genesis pattern.

        Returns:
            The resulting Apex pattern.

        Raises:
            LawViolation: if any substrate law is breached during the sequence.
        """
        self._emit("🔥 Phoenix Ignition Sequence")
        self._emit("─" * 40)

        psi0 = op_genesis(seed)
        self._emit(lambda psi0=psi0: f"  ⊕(∅) → {psi0}")

        psi0_prime = op_harmonic(psi0)
        self._emit(lambda psi0=psi0, psi0_prime=psi0_prime: f"  ⊗({psi0}) → {psi0_prime}")

        psi1 = op_recursive(psi0_prime)
        self._emit(lambda psi0_prime=psi0_prime, psi1=psi1: f"  ⊛({psi0_prime}) → {psi1}")

        psi1_prime = op_harmonic(psi1, amplify=1.5)
        self._emit(lambda psi1=psi1, psi1_prime=psi1_prime: f"  ⊗({psi1}) → {psi1_prime}")

        apex = op_apex(psi1_prime, threshold=self.APEX_THRESHOLD)
        self._emit(lambda psi1_prime=psi1_prime, apex=apex: f"  △({psi1_prime}) → {apex}")
        self._emit("─" * 40)
        self._emit(lambda apex=apex: f"  Apex reached: {apex}")

        return apex

    # ------------------------------------------------------------------
    # Ritual: Phoenix Rebirth Cycle
    # ⊕ → ⊗ → ⊝ → ⊕ → ⊗  (dissolution and renewal)
    # ------------------------------------------------------------------

    def cycle(self, seed: Optional[Any] = None) -> Pattern:
        """
        Execute the Phoenix Rebirth Cycle (dissolution and renewal).

        ⊕ → ⊗ → ⊝ → ⊕ → ⊗

        Args:
            seed: Optional value to seed both the old and renewed patterns.

        Returns:
            The renewed stable pattern after rebirth.
        """
        self._emit("🔄 Phoenix Rebirth Cycle")
        self._emit("─" * 40)

        psi_old = op_genesis(seed, energy=1.0)
        self._emit(lambda psi_old=psi_old: f"  ⊕(∅) → {psi_old}")

        psi_old_prime = op_harmonic(psi_old)
        self._emit(lambda psi_old=psi_old, psi_old_prime=psi_old_prime: f"  ⊗({psi_old}) → {psi_old_prime}")

        void_state = op_void(psi_old_prime)
        self._emit(lambda psi_old_prime=psi_old_prime, void_state=void_state: f"  ⊝({psi_old_prime}) → {void_state}")

        renewed_seed = f"renewed:{seed}" if seed is not None else "renewed"
        psi_new = op_genesis(renewed_seed, energy=1.0)
        self._emit(lambda psi_new=psi_new: f"  ⊕(∅) → {psi_new}  [renewed]")

        psi_new_prime = op_harmonic(psi_new)
        self._emit(lambda psi_new=psi_new, psi_new_prime=psi_new_prime: f"  ⊗({psi_new}) → {psi_new_prime}")

        self._emit("─" * 40)
        self._emit(lambda psi_new_prime=psi_new_prime: f"  Renewal complete: {psi_new_prime}")

        return psi_new_prime

    # ------------------------------------------------------------------
    # Ritual: Convergent Synthesis
    # ⊕×N → ⊳ → ⊗ → ⊛ → ⊗ → △
    # ------------------------------------------------------------------

    def converge(self, seeds: List[Any]) -> Pattern:
        """
        Execute Convergent Synthesis: multiple patterns unified toward Apex.

        ⊕×N → ⊳ → ⊗ → ⊛ → ⊗ → △

        Args:
            seeds: Two or more seed values for Genesis patterns.

        Returns:
            The Apex pattern emerging from unified complexity.

        Raises:
            ValueError:    if fewer than two seeds are provided.
            LawViolation:  if any substrate law is breached.
        """
        if len(seeds) < 2:
            raise ValueError("Convergent synthesis requires at least 2 seeds.")

        self._emit("⊳ Convergent Synthesis")
        self._emit("─" * 40)

        patterns = []
        for s in seeds:
            p = op_genesis(s)
            self._emit(lambda p=p: f"  ⊕(∅) → {p}")
            patterns.append(p)

        unified = op_convergence(*patterns)
        self._emit(lambda patterns=patterns, unified=unified: f"  ⊳({', '.join(str(p) for p in patterns)}) → {unified}")

        stable = op_harmonic(unified)
        self._emit(lambda unified=unified, stable=stable: f"  ⊗({unified}) → {stable}")

        recursive = op_recursive(stable)
        self._emit(lambda stable=stable, recursive=recursive: f"  ⊛({stable}) → {recursive}")

        recursive_stabilized = op_harmonic(recursive, amplify=1.5)
        self._emit(lambda recursive=recursive, recursive_stabilized=recursive_stabilized: f"  ⊗({recursive}) → {recursive_stabilized}")

        apex = op_apex(recursive_stabilized, threshold=self.APEX_THRESHOLD)
        self._emit(lambda recursive_stabilized=recursive_stabilized, apex=apex: f"  △({recursive_stabilized}) → {apex}")
        self._emit("─" * 40)
        self._emit(lambda apex=apex: f"  Apex reached: {apex}")

        return apex

    def get_log(self) -> List[str]:
        """Materialize deferred log entries and return the internal operation log."""
        materialized: List[str] = []
        for index, entry in enumerate(self._log):
            if callable(entry):
                entry = entry()
                self._log[index] = entry
            materialized.append(entry)
        return materialized


# --------------------------------------------------------
# 5. CLI Entry Point
# --------------------------------------------------------

def _banner() -> None:
    print("═" * 55)
    print("   PHOENIX IGNITION ENGINE v2.0.0")
    print("   Transformation  •  Recursion  •  Emergence")
    print("═" * 55)
    print()


def main() -> None:
    """CLI entry point for the Phoenix Ignition Engine."""
    parser = argparse.ArgumentParser(
        description="Phoenix Ignition Engine — The Transformative Core of The Triad",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ignite from void (basic Phoenix sequence)
  %(prog)s --ignite

  # Ignite with a specific seed value
  %(prog)s --ignite --seed "my-pattern"

  # Execute the Phoenix Rebirth Cycle
  %(prog)s --cycle

  # Convergent synthesis of multiple seeds
  %(prog)s --converge seed1 seed2 seed3

For full documentation, see:
  Phoenix/README.md
  Phoenix/rituals/invocation.md
        """,
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--ignite",
        action="store_true",
        help="Execute the basic Phoenix ignition sequence (⊕ → ⊗ → ⊛ → △)",
    )
    group.add_argument(
        "--cycle",
        action="store_true",
        help="Execute the Phoenix Rebirth Cycle (⊕ → ⊗ → ⊝ → ⊕ → ⊗)",
    )
    group.add_argument(
        "--converge",
        nargs="+",
        metavar="SEED",
        help="Execute Convergent Synthesis on the given seeds",
    )

    parser.add_argument(
        "--seed",
        type=str,
        default=None,
        help="Optional seed value for --ignite / --cycle operations",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0",
    )

    args = parser.parse_args()

    _banner()
    engine = PhoenixIgnition(verbose=True)

    try:
        if args.ignite:
            engine.ignite(seed=args.seed)
        elif args.cycle:
            engine.cycle(seed=args.seed)
        elif args.converge:
            engine.converge(seeds=args.converge)
        else:
            parser.print_help()
    except LawViolation as e:
        print(f"\n⚠  Law Violation: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print()
    print("🔥 △ ⚡")
    print()


if __name__ == "__main__":
    main()
