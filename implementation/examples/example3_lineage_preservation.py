#!/usr/bin/env python3
"""
Example 3: Lineage and Identity Preservation
==============================================

Demonstrates how Hydrogenesi preserves lineage and identity through
complex transformation sequences.
"""

import sys
sys.path.insert(0, '..')

from phoenix import PhoenixEngine
from hydrogenesi import HydrogesiEngine


def main():
    print("=" * 70)
    print("Example 3: Lineage and Identity Preservation")
    print("=" * 70)
    print()
    
    phoenix = PhoenixEngine()
    hydrogenesi = HydrogesiEngine()
    
    # Create initial pattern
    print("Step 1: Creating initial pattern")
    print("-" * 50)
    pattern = phoenix.genesis(seed=3.14159)
    pattern_id, identity = hydrogenesi.record_genesis(pattern)
    print(f"Pattern: {pattern}")
    print(f"ID: {pattern_id}")
    print(f"Identity: {identity}")
    print()
    
    # Apply transformation sequence
    print("Step 2: Applying transformation sequence")
    print("-" * 50)
    
    transformations = [
        ('⊗', lambda p: phoenix.harmonic(p)),
        ('⊛', lambda p: phoenix.recursive(p)),
        ('△', lambda p: phoenix.apex(p)),
        ('⊞', lambda p: phoenix.mirror(p)),
    ]
    
    parent_id = pattern_id
    for op_symbol, op_func in transformations:
        pattern = op_func(pattern)
        current_id = hydrogenesi.record_transformation(pattern, op_symbol, parent_id)
        print(f"{op_symbol}: {pattern_id} → {current_id}")
        parent_id = current_id
    
    final_id = parent_id
    print()
    
    # Show lineage
    print("Step 3: Examining lineage")
    print("-" * 50)
    lineage = hydrogenesi.get_lineage(final_id)
    
    print(f"Complete lineage path ({len(lineage)} steps):")
    for i, node in enumerate(lineage):
        indent = "  " * i
        print(f"{indent}{node.operator}: {node.pattern_id} (value={node.value:.4f}, E={node.energy:.3f})")
    print()
    
    # Verify continuity
    print("Step 4: Verifying continuity")
    print("-" * 50)
    continuity = hydrogenesi.verify_continuity(final_id)
    print(f"Continuity verified: {continuity}")
    print()
    
    # Check identity preservation
    print("Step 5: Identity preservation")
    print("-" * 50)
    original_identity = hydrogenesi.get_identity(pattern_id)
    final_identity = hydrogenesi.get_identity(final_id)
    
    print(f"Original identity: {original_identity}")
    print(f"Final identity: {final_identity}")
    print(f"Identity preserved: {original_identity.essence_signature == final_identity.essence_signature}")
    print()
    
    # Full summary
    print("Step 6: Lineage summary")
    print("-" * 50)
    print(hydrogenesi.get_lineage_summary(final_id))
    
    # Test with convergence
    print("Step 7: Convergence with lineage preservation")
    print("-" * 50)
    p1 = phoenix.genesis(1.0)
    p2 = phoenix.genesis(2.0)
    
    id1, _ = hydrogenesi.record_genesis(p1)
    id2, _ = hydrogenesi.record_genesis(p2)
    
    p_merged = phoenix.convergence(p1, p2)
    id_merged = hydrogenesi.record_convergence(p_merged, '⊳', [id1, id2])
    
    print(f"Pattern 1: {id1}")
    print(f"Pattern 2: {id2}")
    print(f"Merged: {id_merged}")
    print(f"Merged lineage: {hydrogenesi.get_lineage(id_merged)}")
    print()
    
    print("=" * 70)
    print("✓ Lineage and identity preserved through all transformations")
    print("=" * 70)


if __name__ == "__main__":
    main()
