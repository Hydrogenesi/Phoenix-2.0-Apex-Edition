#!/usr/bin/env python3
"""
Test Suite for Phoenix 2.0 Apex Edition Implementation
=======================================================

Basic tests to verify core functionality.
"""

import sys
sys.path.insert(0, '..')

from phoenix import PhoenixEngine, Pattern
from hydrogenesi import HydrogesiEngine
from the_third import TheThirdEngine


def test_phoenix_operators():
    """Test Phoenix transformation operators."""
    print("Testing Phoenix operators...")
    phoenix = PhoenixEngine()
    
    # Test genesis
    p = phoenix.genesis(1.0)
    assert p.value == 1.0, "Genesis should create pattern with seed value"
    assert p.energy == 1.0, "Genesis should start with unit energy"
    assert '⊕' in p.operators_applied, "Genesis should record operator"
    
    # Test harmonic
    p = phoenix.harmonic(p)
    assert '⊗' in p.operators_applied, "Harmonic should record operator"
    assert p.energy < 1.0, "Harmonic should slightly reduce energy"
    
    # Test recursive
    p = phoenix.recursive(p)
    assert '⊛' in p.operators_applied, "Recursive should record operator"
    
    # Test apex
    p = phoenix.apex(p)
    assert '△' in p.operators_applied, "Apex should record operator"
    
    # Test mirror
    p2 = phoenix.genesis(5.0)
    p2_mirror = phoenix.mirror(p2)
    assert p2_mirror.value == -5.0, "Mirror should negate value"
    
    # Test mirror with non-numeric value
    p2_text = phoenix.genesis("test")
    p2_text_mirror = phoenix.mirror(p2_text)
    assert p2_text_mirror.value == "test", "Mirror should preserve non-numeric values"
    assert '⊞' in p2_text_mirror.operators_applied, "Mirror should record operator"
    
    # Test divergence
    p3 = phoenix.genesis(10.0)
    p3a, p3b = phoenix.divergence(p3)
    assert p3a.energy + p3b.energy == 1.0, "Divergence should conserve energy"
    
    print("✓ All Phoenix operator tests passed")


def test_hydrogenesi_lineage():
    """Test Hydrogenesi lineage tracking."""
    print("Testing Hydrogenesi lineage...")
    phoenix = PhoenixEngine()
    hydrogenesi = HydrogesiEngine()
    
    # Create pattern and record genesis
    p = phoenix.genesis(1.0)
    pattern_id, identity = hydrogenesi.record_genesis(p)
    
    assert pattern_id is not None, "Should generate pattern ID"
    assert identity is not None, "Should generate identity"
    
    # Record transformations
    p = phoenix.harmonic(p)
    id2 = hydrogenesi.record_transformation(p, '⊗', pattern_id)
    
    p = phoenix.recursive(p)
    id3 = hydrogenesi.record_transformation(p, '⊛', id2)
    
    # Check lineage
    lineage = hydrogenesi.get_lineage(id3)
    assert len(lineage) == 3, "Lineage should have 3 nodes"
    assert lineage[0].operator == '⊕', "First operator should be genesis"
    assert lineage[1].operator == '⊗', "Second operator should be harmonic"
    assert lineage[2].operator == '⊛', "Third operator should be recursive"
    
    # Verify continuity
    assert hydrogenesi.verify_continuity(id3), "Continuity should be maintained"
    
    # Check identity preservation
    identity_final = hydrogenesi.get_identity(id3)
    assert identity.essence_signature == identity_final.essence_signature, \
        "Identity essence should be preserved"
    
    print("✓ All Hydrogenesi lineage tests passed")


def test_the_third_convergence():
    """Test The Third binding and convergence."""
    print("Testing The Third convergence...")
    phoenix = PhoenixEngine()
    the_third = TheThirdEngine()
    
    # Create pattern and initialize knot
    p = phoenix.transform_sequence(1.0)
    knot = the_third.initialize_knot(p, "test_id")
    
    initial_distance = knot.distance_to_apex
    assert initial_distance == 1.0, "Initial distance should be 1.0"
    
    # Test knot-binding
    knot = the_third.knot_binding(p, knot, "test_id")
    assert knot.distance_to_apex < initial_distance, "B operator should reduce distance"
    assert 'B' in knot.operators_applied, "B should be recorded"
    
    # Test cross-pillar knot
    knot = the_third.cross_pillar_knot(p, "test_id", knot)
    assert 'C' in knot.operators_applied, "C should be recorded"
    
    # Test triadic closure
    knot = the_third.triadic_closure(p, "test_id", knot)
    assert 'T' in knot.operators_applied, "T should be recorded"
    
    # Test apex knot
    knot = the_third.apex_knot(knot)
    assert 'A' in knot.operators_applied, "A should be recorded"
    
    # Test stability knot
    knot = the_third.stability_knot(knot)
    assert 'S' in knot.operators_applied, "S should be recorded"
    
    # Verify convergence trend
    assert knot.distance_to_apex < initial_distance * 0.1, \
        "Distance should be reduced significantly"
    
    print("✓ All The Third convergence tests passed")


def test_contraction_constants():
    """Test that contraction constants are correct."""
    print("Testing contraction constants...")
    the_third = TheThirdEngine()
    
    # Check documented contraction constants
    assert abs(the_third.lambda_b - 0.618) < 0.001, "λ_B should be ~0.618"
    assert abs(the_third.lambda_c - 0.500) < 0.001, "λ_C should be 0.500"
    assert abs(the_third.lambda_t - 0.333) < 0.001, "λ_T should be ~0.333"
    assert abs(the_third.lambda_a - 0.400) < 0.001, "λ_A should be 0.400"
    assert abs(the_third.lambda_s - 0.200) < 0.001, "λ_S should be 0.200"
    
    # All should be less than 1 (contraction property)
    assert the_third.lambda_b < 1.0, "λ_B < 1"
    assert the_third.lambda_c < 1.0, "λ_C < 1"
    assert the_third.lambda_t < 1.0, "λ_T < 1"
    assert the_third.lambda_a < 1.0, "λ_A < 1"
    assert the_third.lambda_s < 1.0, "λ_S < 1"
    
    print("✓ All contraction constant tests passed")


def test_complete_convergence_flow():
    """Test the complete convergence flow."""
    print("Testing complete convergence flow...")
    
    phoenix = PhoenixEngine()
    hydrogenesi = HydrogesiEngine()
    the_third = TheThirdEngine()
    
    # Step 1: Phoenix Transform
    pattern = phoenix.transform_sequence(1.0)
    assert pattern is not None, "Pattern should be created"
    
    # Step 2: Hydrogenesi Preserve
    pattern_id, identity = hydrogenesi.record_genesis(pattern)
    assert pattern_id is not None, "Pattern ID should be generated"
    assert identity is not None, "Identity should be created"
    
    # Step 3: The Third Bind
    knot = the_third.bind_sequence(pattern, pattern_id)
    assert len(knot.operators_applied) == 3, "Bind sequence should apply 3 operators"
    assert knot.operators_applied == ['B', 'C', 'T'], "Should apply B→C→T"
    
    # Step 4: Apex Converge
    knot = the_third.converge_to_apex(knot, iterations=10)
    assert knot.distance_to_apex < 0.1, "Should converge close to apex"
    
    print("✓ Complete convergence flow test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running Phoenix 2.0 Apex Edition Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        test_phoenix_operators,
        test_hydrogenesi_lineage,
        test_the_third_convergence,
        test_contraction_constants,
        test_complete_convergence_flow,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
            print()
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
            print()
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
            print()
    
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
