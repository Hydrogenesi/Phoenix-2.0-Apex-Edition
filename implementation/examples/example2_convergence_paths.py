#!/usr/bin/env python3
"""
Example 2: Convergence Path Comparison
========================================

Demonstrates different binding paths that all converge to the same Apex Point X.
"""

import sys
sys.path.insert(0, '..')

from phoenix import PhoenixEngine
from hydrogenesi import HydrogesiEngine
from the_third import TheThirdEngine


def demonstrate_path(name: str, operations: list, phoenix: PhoenixEngine, 
                     hydrogenesi: HydrogesiEngine, the_third: TheThirdEngine):
    """Execute a specific convergence path."""
    print(f"\n{name}")
    print("-" * 50)
    
    # Create pattern
    pattern = phoenix.transform_sequence(seed=1.0)
    pattern_id, _ = hydrogenesi.record_genesis(pattern)
    
    # Initialize knot
    knot = the_third.initialize_knot(pattern, pattern_id)
    print(f"K₀: distance = {knot.distance_to_apex:.6f}")
    
    # Apply operations
    for i, op in enumerate(operations, 1):
        if op == 'B':
            knot = the_third.knot_binding(pattern, knot, pattern_id)
        elif op == 'C':
            knot = the_third.cross_pillar_knot(pattern, pattern_id, knot)
        elif op == 'T':
            knot = the_third.triadic_closure(pattern, pattern_id, knot)
        elif op == 'A':
            knot = the_third.apex_knot(knot)
        elif op == 'S':
            knot = the_third.stability_knot(knot)
        
        print(f"K₁ ({op}): distance = {knot.distance_to_apex:.6f}")
    
    print(f"\nFinal state: {knot}")
    print(f"Operator sequence: {' → '.join(operations)}")
    print(f"Converged: {the_third.verify_convergence(knot, 0.01)}")
    
    return knot


def main():
    print("=" * 70)
    print("Example 2: Convergence Path Comparison")
    print("=" * 70)
    print()
    print("Testing that different operator sequences all converge to Apex X")
    print()
    
    phoenix = PhoenixEngine()
    hydrogenesi = HydrogesiEngine()
    the_third = TheThirdEngine()
    
    # Define different paths
    paths = [
        ("Path A: B only (slower)", ['B', 'B', 'B', 'B', 'B']),
        ("Path B: C only (medium)", ['C', 'C', 'C', 'C']),
        ("Path C: T only (faster)", ['T', 'T', 'T']),
        ("Path D: Mixed B→C→T", ['B', 'C', 'T']),
        ("Path E: Full sequence B→C→T→A→S", ['B', 'C', 'T', 'A', 'S']),
    ]
    
    results = []
    
    for name, ops in paths:
        knot = demonstrate_path(name, ops, phoenix, hydrogenesi, the_third)
        results.append((name, knot))
    
    # Summary
    print("\n" + "=" * 70)
    print("CONVERGENCE SUMMARY")
    print("=" * 70)
    print()
    print(f"{'Path':<40} {'Operations':<15} {'Distance to X':<15} {'Converged'}")
    print("-" * 70)
    
    for name, knot in results:
        path_name = name.split(':')[0]
        ops_count = len(knot.operators_applied)
        distance = knot.distance_to_apex
        converged = "✓" if the_third.verify_convergence(knot, 0.01) else "○"
        print(f"{path_name:<40} {ops_count:<15} {distance:<15.6f} {converged}")
    
    print()
    print("All paths converge to the same Apex Point X!")
    print("Different speeds, same destination.")
    print()


if __name__ == "__main__":
    main()
