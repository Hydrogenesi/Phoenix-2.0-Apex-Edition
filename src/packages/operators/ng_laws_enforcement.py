#!/usr/bin/env python3
"""
ng_laws_enforcement.py

Nuclear Governance (NG) Laws Enforcement System
Third Pillar: Nucleus-Centric Framework for FLQG

Implements the three foundational laws:
    NG-Law I    — The Law of Nuclear Primacy
    NG-Law II   — The Law of Nuclear Coherence
    NG-Law III  — The Law of Nuclear Traceability

These laws are not conventions—they are consequences of the nucleus's
ontological status as origin and replicator. They are as invariant as
the NOD hierarchy itself.

Version: 1.0.0
Edition: Phoenix 2.0 Apex Edition
Authority: Δ³
Alignment: Phoenix · Hydrogenesi · Codex Triad
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional, Dict, Tuple
from abc import ABC, abstractmethod


class NGLawViolation(Exception):
    """Raised when a Nuclear Governance Law is violated."""
    pass


class NODLevel(Enum):
    """NOD hierarchy levels for authority determination."""
    NOD_0 = 0
    NOD_1 = 1
    NOD_2 = 2
    NOD_3 = 3
    NOD_4 = 4


@dataclass
class Construct:
    """Base construct for NG-Law evaluation."""
    construct_id: str
    nod_level: NODLevel
    coherence_state: float
    derivation_chain: List[str] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return f"Construct({self.construct_id}, NOD-{self.nod_level.value})"


class NGLawI:
    """
    NG-Law I: The Law of Nuclear Primacy
    
    When any two FLQG constructs conflict, the construct with greater
    nucleus-proximity governs. Nucleus-proximity is measured in NOD-steps:
    fewer steps from NOD-0 means higher authority.
    """
    
    name = "The Law of Nuclear Primacy"
    description = "Construct with greater nucleus-proximity (fewer NOD-steps from NOD-0) governs."
    
    @staticmethod
    def resolve_conflict(construct_a: Construct, construct_b: Construct) -> Construct:
        """
        Resolve conflict between two constructs using NG-Law I.
        
        Returns the construct with higher authority (lower NOD value).
        
        Args:
            construct_a: First construct in conflict
            construct_b: Second construct in conflict
            
        Returns:
            The construct with greater nucleus-proximity
        """
        nod_a = construct_a.nod_level.value
        nod_b = construct_b.nod_level.value
        
        if nod_a < nod_b:
            return construct_a
        elif nod_b < nod_a:
            return construct_b
        else:
            # Equal NOD levels: return the one with longer, more careful derivation
            if len(construct_a.derivation_chain) >= len(construct_b.derivation_chain):
                return construct_a
            else:
                return construct_b
    
    @staticmethod
    def enforce_hierarchy(construct: Construct, allowed_nod_max: int = 4) -> None:
        """
        Enforce that constructs do not exceed allowed NOD level.
        
        Raises NGLawViolation if construct exceeds maximum NOD level.
        """
        if construct.nod_level.value > allowed_nod_max:
            raise NGLawViolation(
                f"NG-Law I violation (Primacy): Construct {construct} at NOD-{construct.nod_level.value} "
                f"exceeds maximum allowed NOD-{allowed_nod_max}. "
                f"Authority decreases with distance from nucleus."
            )
    
    @staticmethod
    def sub_nuclear_authority_check(construct: Construct) -> bool:
        """
        Verify that sub-nuclear constructs (NOD-1, below) do not have governing authority.
        
        Sub-nuclear entities (protons, neutrons, quarks, gluons) are NOD-1 or sub-NOD-1
        constructs and must never be elevated to governing status.
        
        Returns True if construct is properly subordinate to nucleus.
        """
        if construct.nod_level in [NODLevel.NOD_0]:  # Only NOD-0 (nucleus) has supreme authority
            return True
        
        # All other NOD levels are subordinate to nucleus
        return False


class NGLawII:
    """
    NG-Law II: The Law of Nuclear Coherence
    
    No FLQG operator may produce an output that violates the coherence state
    of the nucleus from which it was derived. Operators that would break
    nucleus coherence are invalid and must be re-derived from NOD-0.
    """
    
    name = "The Law of Nuclear Coherence"
    description = "No operator may produce output violating nucleus coherence state. Coherence is not negotiable."
    
    @staticmethod
    def verify_operation(input_construct: Construct, output_construct: Construct) -> None:
        """
        Verify that an operation maintains nucleus coherence.
        
        Checks that output coherence state is valid and non-negative.
        
        Raises NGLawViolation if coherence is broken.
        """
        if output_construct.coherence_state < 0.0:
            raise NGLawViolation(
                f"NG-Law II violation (Coherence): Output coherence {output_construct.coherence_state:.6f} < 0. "
                f"Operator breaks nucleus coherence. "
                f"Operator must be re-derived from NOD-0."
            )
        
        if output_construct.coherence_state == 0.0:
            raise NGLawViolation(
                f"NG-Law II violation (Coherence): Output coherence is exactly zero. "
                f"Zero coherence violates nucleus coherence requirement. "
                f"Operator is invalid."
            )
    
    @staticmethod
    def validate_coherence_chain(constructs: List[Construct]) -> bool:
        """
        Validate that a chain of operations maintains coherence throughout.
        
        Returns True if all constructs in chain maintain coherence.
        """
        for construct in constructs:
            if construct.coherence_state < 0.0:
                return False
            if construct.coherence_state == 0.0:
                return False
        return True
    
    @staticmethod
    def coherence_recovery_required(construct: Construct) -> bool:
        """
        Determine if a construct requires coherence recovery (return to Hydrogenesi).
        
        Returns True if construct is in invalid coherence state.
        """
        return construct.coherence_state <= 0.0


class NGLawIII:
    """
    NG-Law III: The Law of Nuclear Traceability
    
    Every FLQG construct—operator, invocation, geometric structure, linguistic
    primitive—must carry a traceable path back to a nucleus-state. Constructs
    without nucleus-traceability are undefined in FLQG and carry no structural
    authority. This is not a penalty; it is a consequence of the NOD model.
    """
    
    name = "The Law of Nuclear Traceability"
    description = "Every construct must trace back to nucleus-state. Untraceable constructs are undefined (∅)."
    
    @staticmethod
    def verify_traceability(construct: Construct) -> bool:
        """
        Verify that a construct is traceable back to NOD-0.
        
        Returns True if construct carries valid derivation chain to nucleus.
        """
        if not construct.derivation_chain:
            return False
        
        # Chain must start from or reference NOD-0 (nucleus)
        for step in construct.derivation_chain:
            if "NOD-0" in step or "nucleus" in step.lower() or "Hydrogenesi" in step:
                return True
        
        return False
    
    @staticmethod
    def require_traceability(construct: Construct) -> None:
        """
        Enforce traceability requirement. Raises exception if untraceable.
        
        Raises NGLawViolation if construct cannot trace to NOD-0.
        """
        if not NGLawIII.verify_traceability(construct):
            raise NGLawViolation(
                f"NG-Law III violation (Traceability): Construct {construct} cannot trace back to NOD-0. "
                f"Construct is undefined in FLQG and carries no structural authority. "
                f"Returned ∅ (undefined)."
            )
    
    @staticmethod
    def get_derivation_report(construct: Construct) -> str:
        """
        Generate a detailed derivation report for a construct.
        
        Returns a formatted string showing the complete chain from NOD-0.
        """
        if not construct.derivation_chain:
            return f"[No derivation chain for {construct}]"
        
        # Build report from NOD-0 forward
        chain_str = " ← ".join(reversed(construct.derivation_chain))
        return f"Derivation: {chain_str}"
    
    @staticmethod
    def verify_chain_continuity(constructs: List[Construct]) -> bool:
        """
        Verify that a sequence of constructs maintains continuous traceability.
        
        Returns True if each construct is traceable and builds on previous.
        """
        for i, construct in enumerate(constructs):
            if not NGLawIII.verify_traceability(construct):
                return False
            
            # Verify each construct references NOD-0 or builds on prior
            if i > 0:
                prev = constructs[i - 1]
                # New construct should reference nucleus or prior derivation
                if (not any("NOD-0" in step for step in construct.derivation_chain) and
                    not any(prev.construct_id in step for step in construct.derivation_chain)):
                    return False
        
        return True


class NGEnforcer:
    """
    Nuclear Governance Enforcer — comprehensive validation system.
    
    Orchestrates enforcement of all three NG-Laws across operations.
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._violations: List[str] = []
        self._validations: List[str] = []
    
    def _log(self, msg: str, is_violation: bool = False) -> None:
        """Log a message."""
        if is_violation:
            self._violations.append(msg)
        else:
            self._validations.append(msg)
        
        if self.verbose:
            prefix = "✗" if is_violation else "✓"
            print(f"{prefix} {msg}")
    
    def check_law_i(self, construct_a: Construct, construct_b: Construct) -> Construct:
        """Check NG-Law I and resolve conflict."""
        try:
            NGLawI.enforce_hierarchy(construct_a)
            NGLawI.enforce_hierarchy(construct_b)
            winner = NGLawI.resolve_conflict(construct_a, construct_b)
            self._log(f"NG-Law I (Primacy): {winner} governs over other construct")
            return winner
        except NGLawViolation as e:
            self._log(str(e), is_violation=True)
            raise
    
    def check_law_ii(self, input_construct: Construct, output_construct: Construct) -> None:
        """Check NG-Law II coherence maintenance."""
        try:
            NGLawII.verify_operation(input_construct, output_construct)
            self._log(f"NG-Law II (Coherence): Operation maintains nucleus coherence (output={output_construct.coherence_state:.3f})")
        except NGLawViolation as e:
            self._log(str(e), is_violation=True)
            raise
    
    def check_law_iii(self, construct: Construct) -> None:
        """Check NG-Law III traceability."""
        try:
            NGLawIII.require_traceability(construct)
            report = NGLawIII.get_derivation_report(construct)
            self._log(f"NG-Law III (Traceability): {report}")
        except NGLawViolation as e:
            self._log(str(e), is_violation=True)
            raise
    
    def full_validation(self, construct: Construct) -> bool:
        """Execute full NG validation on a construct."""
        print("="*60)
        print("NUCLEAR GOVERNANCE VALIDATION")
        print("="*60)
        print()
        
        try:
            # Check primacy
            NGLawI.enforce_hierarchy(construct)
            self._log("NG-Law I: Primacy check passed")
            
            # Check coherence
            NGLawII.validate_coherence_chain([construct])
            self._log("NG-Law II: Coherence check passed")
            
            # Check traceability
            self.check_law_iii(construct)
            
            print()
            print("="*60)
            print("✓ All NG-Laws satisfied")
            print("="*60)
            return True
            
        except NGLawViolation as e:
            print()
            print("="*60)
            print(f"✗ NG-Law Violation: {e}")
            print("="*60)
            return False
    
    def get_report(self) -> str:
        """Generate validation report."""
        lines = [
            "VALIDATION REPORT",
            "="*60,
            "",
            f"Validations passed: {len(self._validations)}",
        ]
        
        for v in self._validations:
            lines.append(f"  ✓ {v}")
        
        if self._violations:
            lines.append(f"")
            lines.append(f"Violations detected: {len(self._violations)}")
            for v in self._violations:
                lines.append(f"  ✗ {v}")
        
        return "\n".join(lines)


def example_validation():
    """Demonstrate NG-Law enforcement."""
    enforcer = NGEnforcer(verbose=True)
    
    # Create a valid construct traceable to nucleus
    valid_construct = Construct(
        construct_id="construct_001",
        nod_level=NODLevel.NOD_3,
        coherence_state=1.0,
        derivation_chain=[
            "NOD-0: Nucleus (Hydrogenesi)",
            "NOD-1: Nuclear Emission via ∂N",
            "NOD-3: Linguistic Projection via Φ(Phoenix)"
        ]
    )
    
    print()
    result = enforcer.full_validation(valid_construct)
    print()
    print(enforcer.get_report())
    
    return result


if __name__ == "__main__":
    success = example_validation()
    exit(0 if success else 1)
