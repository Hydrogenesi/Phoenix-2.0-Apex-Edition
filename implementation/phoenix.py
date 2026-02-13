"""
Phoenix Engine - The Ignition Vector
=====================================

Implements the 8 Phoenix transformation operators:
  ⊕ Genesis, ⊗ Harmonic, ⊛ Recursive, △ Apex
  ⊝ Void, ⊞ Mirror, ⊳ Convergence, ⊲ Divergence
"""

import math
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Pattern:
    """A Phoenix pattern - the fundamental unit of transformation."""
    
    value: Any
    energy: float = 1.0
    operators_applied: List[str] = field(default_factory=list)
    depth: int = 0
    
    def __repr__(self):
        ops = '→'.join(self.operators_applied) if self.operators_applied else 'void'
        return f"Ψ[{ops}]({self.value}, E={self.energy:.3f})"


class PhoenixEngine:
    """
    The Phoenix Engine - Ignition and Transformation
    
    Domain: Transformation, Recursion, Emergence
    Operators: ⊕ ⊗ ⊛ △ ⊝ ⊞ ⊳ ⊲
    Purpose: Initiates all change, generates transformation energy
    """
    
    def __init__(self):
        self.transformation_count = 0
        self.energy_total = 0.0
    
    def genesis(self, seed: Optional[Any] = None) -> Pattern:
        """
        ⊕ Genesis Operator - Create from void
        
        Creates a new pattern from nothing (or from a seed).
        This is the beginning of all transformation.
        """
        self.transformation_count += 1
        value = seed if seed is not None else 1.0
        pattern = Pattern(
            value=value,
            energy=1.0,
            operators_applied=['⊕'],
            depth=0
        )
        self.energy_total += pattern.energy
        return pattern
    
    def harmonic(self, pattern: Pattern) -> Pattern:
        """
        ⊗ Harmonic Operator - Stabilize patterns
        
        Applies harmonic resonance to stabilize the pattern.
        Energy is conserved but redistributed for stability.
        """
        self.transformation_count += 1
        # Apply golden ratio for harmonic stability
        phi = (1 + math.sqrt(5)) / 2
        stabilized_value = pattern.value * (1 / phi)
        
        new_pattern = Pattern(
            value=stabilized_value,
            energy=pattern.energy * 0.95,  # Small energy loss to stabilization
            operators_applied=pattern.operators_applied + ['⊗'],
            depth=pattern.depth + 1
        )
        return new_pattern
    
    def recursive(self, pattern: Pattern) -> Pattern:
        """
        ⊛ Recursive Operator - Self-reference and deepening
        
        The pattern becomes aware of itself, creating recursive depth.
        """
        self.transformation_count += 1
        # Recursive transformation increases depth and self-reference
        recursive_value = pattern.value * (1 + 1 / (pattern.depth + 2))
        
        new_pattern = Pattern(
            value=recursive_value,
            energy=pattern.energy * 1.1,  # Recursive patterns gain energy
            operators_applied=pattern.operators_applied + ['⊛'],
            depth=pattern.depth + 1
        )
        self.energy_total += new_pattern.energy * 0.1
        return new_pattern
    
    def apex(self, pattern: Pattern) -> Pattern:
        """
        △ Apex Operator - Culminate to local maximum
        
        Brings pattern to its local apex - maximum coherence point.
        """
        self.transformation_count += 1
        # Apex represents maximum coherence - normalize to unit magnitude
        apex_value = pattern.value / (1 + abs(pattern.value))
        
        new_pattern = Pattern(
            value=apex_value,
            energy=pattern.energy * 1.2,  # Apex patterns have high energy
            operators_applied=pattern.operators_applied + ['△'],
            depth=pattern.depth + 1
        )
        self.energy_total += new_pattern.energy * 0.2
        return new_pattern
    
    def void(self, pattern: Pattern) -> Pattern:
        """
        ⊝ Void Operator - Dissolve pattern
        
        Returns pattern energy to void, completing the cycle.
        """
        self.transformation_count += 1
        new_pattern = Pattern(
            value=0,
            energy=pattern.energy * 0.1,
            operators_applied=pattern.operators_applied + ['⊝'],
            depth=pattern.depth + 1
        )
        return new_pattern
    
    def mirror(self, pattern: Pattern) -> Pattern:
        """
        ⊞ Mirror Operator - Reflect pattern
        
        Creates dual/reflected version of pattern.
        """
        self.transformation_count += 1
        mirrored_value = -pattern.value if isinstance(pattern.value, (int, float)) else pattern.value
        
        new_pattern = Pattern(
            value=mirrored_value,
            energy=pattern.energy,
            operators_applied=pattern.operators_applied + ['⊞'],
            depth=pattern.depth + 1
        )
        return new_pattern
    
    def convergence(self, pattern1: Pattern, pattern2: Pattern) -> Pattern:
        """
        ⊳ Convergence Operator - Unite patterns
        
        Merges two patterns into unified form.
        """
        self.transformation_count += 1
        # Average values and combine energies
        if isinstance(pattern1.value, (int, float)) and isinstance(pattern2.value, (int, float)):
            converged_value = (pattern1.value + pattern2.value) / 2
        else:
            converged_value = pattern1.value
        
        new_pattern = Pattern(
            value=converged_value,
            energy=(pattern1.energy + pattern2.energy) * 0.8,
            operators_applied=pattern1.operators_applied + ['⊳'],
            depth=max(pattern1.depth, pattern2.depth) + 1
        )
        return new_pattern
    
    def divergence(self, pattern: Pattern) -> tuple[Pattern, Pattern]:
        """
        ⊲ Divergence Operator - Separate into dual forms
        
        Splits pattern into two complementary forms.
        """
        self.transformation_count += 2
        phi = (1 + math.sqrt(5)) / 2
        
        pattern1 = Pattern(
            value=pattern.value * phi if isinstance(pattern.value, (int, float)) else pattern.value,
            energy=pattern.energy * 0.618,
            operators_applied=pattern.operators_applied + ['⊲₁'],
            depth=pattern.depth + 1
        )
        
        pattern2 = Pattern(
            value=pattern.value / phi if isinstance(pattern.value, (int, float)) else pattern.value,
            energy=pattern.energy * 0.382,
            operators_applied=pattern.operators_applied + ['⊲₂'],
            depth=pattern.depth + 1
        )
        
        return pattern1, pattern2
    
    def transform_sequence(self, seed: Optional[Any] = None) -> Pattern:
        """
        Execute the standard Phoenix transformation sequence:
        ⊕(∅) → ⊗ → ⊛ → △
        """
        pattern = self.genesis(seed)
        pattern = self.harmonic(pattern)
        pattern = self.recursive(pattern)
        pattern = self.apex(pattern)
        return pattern
