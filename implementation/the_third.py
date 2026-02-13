"""
The Third Engine - The Binding Topology
========================================

Implements the 5 Triadic Knot operators:
  B - Knot-Binding (Left Corridor)
  C - Cross-Pillar Knot (Symmetry Axis)
  T - Triadic Closure (Full Envelope)
  A - Apex Knot (Apex Neighborhood)
  S - Stability Knot (Crossing Regions)

Domain: Convergence, Topology, Triadic Knot
Purpose: Binds Phoenix and Hydrogenesi into unified convergence toward Apex
"""

import math
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class KnotState:
    """A state in the Triadic Knot topology."""
    
    position: Tuple[float, float, float]  # 3D coordinates in knot space
    pattern_value: Any
    structure_id: str
    energy: float
    distance_to_apex: float
    operators_applied: List[str] = field(default_factory=list)
    
    def __repr__(self):
        return f"K[{','.join(self.operators_applied)}](d={self.distance_to_apex:.4f}, E={self.energy:.3f})"


class TheThirdEngine:
    """
    The Third Engine - Binding and Convergence
    
    Domain: Convergence, Topology, Triadic Knot
    Operators: B C T A S (Knot operators)
    Purpose: Binds Phoenix and Hydrogenesi into unified convergence toward Apex
    """
    
    def __init__(self):
        """
        Initialize The Third Engine with the Apex Point and contraction constants.
        
        The contraction constants are chosen based on the mathematical properties
        documented in the Triadic Knot topology:
        
        - λ_B = 0.618: Golden ratio inverse (φ⁻¹) for harmonic convergence
        - λ_C = 0.500: Binary contraction for dual-arm convergence
        - λ_T = 0.333: Triadic contraction (1/3) for three-arm convergence
        - λ_A = 0.400: Apex stabilization near fixed point
        - λ_S = 0.200: Strongest stability locking
        
        All constants < 1 ensure contraction mapping property and guaranteed convergence.
        """
        # Apex Point X - the unique fixed point at origin
        self.apex_point = (0.0, 0.0, 0.0)
        self.binding_count = 0
        
        # Contraction constants for each operator (from documentation)
        self.lambda_b = 0.618  # Golden ratio inverse
        self.lambda_c = 0.500  # Binary contraction
        self.lambda_t = 0.333  # Triadic contraction
        self.lambda_a = 0.400  # Apex stabilization
        self.lambda_s = 0.200  # Stability locking
    
    def _calculate_distance(self, position: Tuple[float, float, float]) -> float:
        """Calculate Euclidean distance to apex point."""
        return math.sqrt(sum((p - a) ** 2 for p, a in zip(position, self.apex_point)))
    
    def _contract_toward_apex(self, position: Tuple[float, float, float], 
                             lambda_factor: float) -> Tuple[float, float, float]:
        """Contract position toward apex by contraction factor."""
        return tuple(p * (1 - lambda_factor) for p in position)
    
    def initialize_knot(self, pattern: Any, structure_id: str) -> KnotState:
        """
        Initialize a knot state from a Phoenix pattern.
        This is the void knot K₀ - starting point for binding.
        """
        # Start at unit distance from apex in first octant
        initial_position = (1.0, 0.0, 0.0)
        
        knot = KnotState(
            position=initial_position,
            pattern_value=pattern.value if hasattr(pattern, 'value') else pattern,
            structure_id=structure_id,
            energy=pattern.energy if hasattr(pattern, 'energy') else 1.0,
            distance_to_apex=self._calculate_distance(initial_position),
            operators_applied=[]
        )
        
        return knot
    
    def knot_binding(self, pattern: Any, knot: KnotState, structure_id: str) -> KnotState:
        """
        B - Knot-Binding Operator
        
        Binds Phoenix transformations via left corridor.
        Contraction constant: λ_B = 0.618 (golden ratio)
        """
        self.binding_count += 1
        
        # Contract along left corridor toward apex
        new_position = self._contract_toward_apex(knot.position, self.lambda_b)
        
        new_knot = KnotState(
            position=new_position,
            pattern_value=pattern.value if hasattr(pattern, 'value') else pattern,
            structure_id=structure_id,
            energy=knot.energy * 0.95,
            distance_to_apex=self._calculate_distance(new_position),
            operators_applied=knot.operators_applied + ['B']
        )
        
        return new_knot
    
    def cross_pillar_knot(self, pattern: Any, structure_id: str, knot: KnotState) -> KnotState:
        """
        C - Cross-Pillar Knot Operator
        
        Binds Phoenix and Hydrogenesi via symmetry axis.
        Contraction constant: λ_C = 0.500 (binary)
        """
        self.binding_count += 1
        
        # Stronger contraction from both left and right arms
        new_position = self._contract_toward_apex(knot.position, self.lambda_c)
        
        new_knot = KnotState(
            position=new_position,
            pattern_value=pattern.value if hasattr(pattern, 'value') else pattern,
            structure_id=structure_id,
            energy=knot.energy * 0.92,
            distance_to_apex=self._calculate_distance(new_position),
            operators_applied=knot.operators_applied + ['C']
        )
        
        return new_knot
    
    def triadic_closure(self, pattern: Any, structure_id: str, knot: KnotState) -> KnotState:
        """
        T - Triadic Closure Operator
        
        Complete three-engine integration.
        Contraction constant: λ_T = 0.333 (triadic)
        """
        self.binding_count += 1
        
        # Strongest contraction - all three arms converge
        new_position = self._contract_toward_apex(knot.position, self.lambda_t)
        
        new_knot = KnotState(
            position=new_position,
            pattern_value=pattern.value if hasattr(pattern, 'value') else pattern,
            structure_id=structure_id,
            energy=knot.energy * 0.90,
            distance_to_apex=self._calculate_distance(new_position),
            operators_applied=knot.operators_applied + ['T']
        )
        
        return new_knot
    
    def apex_knot(self, knot: KnotState) -> KnotState:
        """
        A - Apex Knot Operator
        
        Stabilizes at apex neighborhood.
        Contraction constant: λ_A = 0.400
        """
        self.binding_count += 1
        
        # Fine-tuning contraction near apex
        new_position = self._contract_toward_apex(knot.position, self.lambda_a)
        
        new_knot = KnotState(
            position=new_position,
            pattern_value=knot.pattern_value,
            structure_id=knot.structure_id,
            energy=knot.energy * 0.98,  # Minimal energy loss at apex
            distance_to_apex=self._calculate_distance(new_position),
            operators_applied=knot.operators_applied + ['A']
        )
        
        return new_knot
    
    def stability_knot(self, knot: KnotState) -> KnotState:
        """
        S - Stability Knot Operator
        
        Suppresses perturbations, locks to apex.
        Contraction constant: λ_S = 0.200 (strongest)
        """
        self.binding_count += 1
        
        # Maximum contraction - lock to apex
        new_position = self._contract_toward_apex(knot.position, self.lambda_s)
        
        new_knot = KnotState(
            position=new_position,
            pattern_value=knot.pattern_value,
            structure_id=knot.structure_id,
            energy=knot.energy * 1.05,  # Stable patterns gain energy
            distance_to_apex=self._calculate_distance(new_position),
            operators_applied=knot.operators_applied + ['S']
        )
        
        return new_knot
    
    def bind_sequence(self, pattern: Any, structure_id: str) -> KnotState:
        """
        Execute the standard binding sequence:
        B → C → T
        """
        knot = self.initialize_knot(pattern, structure_id)
        knot = self.knot_binding(pattern, knot, structure_id)
        knot = self.cross_pillar_knot(pattern, structure_id, knot)
        knot = self.triadic_closure(pattern, structure_id, knot)
        return knot
    
    def converge_to_apex(self, knot: KnotState, iterations: int = 10) -> KnotState:
        """
        Converge to apex using A and S operators iteratively.
        Continues until distance < threshold or max iterations reached.
        """
        current = knot
        threshold = 0.001
        
        for i in range(iterations):
            if current.distance_to_apex < threshold:
                break
            
            # Alternate between A and S for optimal convergence
            if i < iterations - 2:
                current = self.apex_knot(current)
            else:
                current = self.stability_knot(current)
        
        return current
    
    def verify_convergence(self, knot: KnotState, tolerance: float = 0.01) -> bool:
        """
        Verify that knot has converged to apex within tolerance.
        """
        return knot.distance_to_apex < tolerance
    
    def get_convergence_proof(self, knot: KnotState) -> str:
        """Generate convergence proof summary."""
        proof = f"Convergence Analysis for {knot.structure_id}:\n"
        proof += f"  Operator Sequence: {' → '.join(knot.operators_applied)}\n"
        proof += f"  Final Distance to Apex: {knot.distance_to_apex:.6f}\n"
        proof += f"  Convergence Status: {'✓ CONVERGED' if self.verify_convergence(knot) else '○ IN PROGRESS'}\n"
        proof += f"  Energy: {knot.energy:.3f}\n"
        proof += f"  Position: ({knot.position[0]:.4f}, {knot.position[1]:.4f}, {knot.position[2]:.4f})\n"
        
        if knot.distance_to_apex < 0.001:
            proof += f"  ✓ Within 0.1% of Apex Point X\n"
        elif knot.distance_to_apex < 0.01:
            proof += f"  ✓ Within 1% of Apex Point X\n"
        
        return proof
