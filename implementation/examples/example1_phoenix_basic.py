#!/usr/bin/env python3
"""
Example 1: Basic Phoenix Transformation Sequence
=================================================

Demonstrates the fundamental Phoenix operators in sequence.
"""

import sys
sys.path.insert(0, '..')

from phoenix import PhoenixEngine


def main():
    print("=" * 70)
    print("Example 1: Basic Phoenix Transformation Sequence")
    print("=" * 70)
    print()
    
    phoenix = PhoenixEngine()
    
    # Standard sequence: ⊕ → ⊗ → ⊛ → △
    print("Executing standard Phoenix transformation sequence...")
    print()
    
    pattern = phoenix.transform_sequence(seed=2.0)
    
    print(f"Final pattern: {pattern}")
    print(f"Transformations applied: {phoenix.transformation_count}")
    print(f"Total energy: {phoenix.energy_total:.3f}")
    print()
    
    # Individual operations
    print("-" * 70)
    print("Individual operator demonstrations:")
    print()
    
    # Genesis from different seeds
    print("⊕ Genesis from different seeds:")
    for seed in [1.0, 5.0, 10.0]:
        p = phoenix.genesis(seed)
        print(f"  seed={seed} → {p}")
    print()
    
    # Mirror demonstration
    print("⊞ Mirror operator:")
    p = phoenix.genesis(5.0)
    p_mirror = phoenix.mirror(p)
    print(f"  Original: {p}")
    print(f"  Mirror: {p_mirror}")
    print()
    
    # Divergence demonstration
    print("⊲ Divergence operator:")
    p = phoenix.genesis(10.0)
    p1, p2 = phoenix.divergence(p)
    print(f"  Original: {p}")
    print(f"  Split 1: {p1}")
    print(f"  Split 2: {p2}")
    print()
    
    # Convergence demonstration
    print("⊳ Convergence operator:")
    merged = phoenix.convergence(p1, p2)
    print(f"  Pattern 1: {p1}")
    print(f"  Pattern 2: {p2}")
    print(f"  Merged: {merged}")
    print()
    
    print("=" * 70)
    print("✓ Example complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
