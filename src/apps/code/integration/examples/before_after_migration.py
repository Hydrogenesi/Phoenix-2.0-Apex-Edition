#!/usr/bin/env python3
"""
Before/After Migration Example — Integration Engine v2.0.0

Demonstrates migration from v1.x basic waltz to v2.0.0 production-ready engine.
"""

from integration_engine import (
    ThreeFingerWaltz,
    CachedThreeFingerWaltz,
    InstrumentedThreeFingerWaltz,
    IntegrationEngine,
)

# Example patterns for demonstration
patterns = [
    {"id": "pattern_1", "type": "transformation", "data": [1, 2, 3]},
    {"id": "pattern_2", "type": "harmonic", "data": [4, 5, 6]},
    {"id": "pattern_3", "type": "recursive", "data": [7, 8, 9]},
]


def v1_style():
    """v1.x style: basic waltz execution"""
    print("=" * 60)
    print("V1.X STYLE: Basic Three-Finger Waltz")
    print("=" * 60)
    
    waltz_v1 = ThreeFingerWaltz(patterns=patterns)
    result_v1 = waltz_v1.dance()
    
    print(f"Result: {result_v1}")
    print("✓ Works, but no observability, no optimization")
    print()
    return result_v1


def v2_minimal():
    """v2.0.0 minimal migration: direct replacement"""
    print("=" * 60)
    print("V2.0.0 MINIMAL: Direct Replacement")
    print("=" * 60)
    
    # Minimal change: disable all v2 features for compatibility
    engine = IntegrationEngine(enable_cache=False, enable_telemetry=False)
    result_v2 = engine.integrate(patterns)
    
    print(f"Result: {result_v2}")
    print("✓ Drop-in replacement with same behavior")
    print()
    return result_v2


def v2_cached():
    """v2.0.0 with caching enabled"""
    print("=" * 60)
    print("V2.0.0 WITH CACHING: Performance Layer")
    print("=" * 60)
    
    engine = IntegrationEngine(enable_cache=True, enable_telemetry=False)
    
    # First call: cold cache
    result1 = engine.integrate(patterns)
    print(f"First call (cold cache): {result1}")
    
    # Second call: warm cache
    result2 = engine.integrate(patterns)
    print(f"Second call (warm cache): {result2}")
    
    stats = engine.get_cache_stats()
    print(f"Cache stats: {stats}")
    print("✓ Cached results improve performance")
    print()
    return result2


def v2_full():
    """v2.0.0 full production: caching + telemetry"""
    print("=" * 60)
    print("V2.0.0 FULL PRODUCTION: Cache + Telemetry")
    print("=" * 60)
    
    import logging
    logging.basicConfig(level=logging.INFO)
    
    engine = IntegrationEngine(
        enable_cache=True,
        enable_telemetry=True,
        cache_size=128,
        log_level=logging.INFO,
    )
    
    result = engine.integrate(patterns)
    
    print(f"Result: {result}")
    print(f"Cache stats: {engine.get_cache_stats()}")
    print(f"Metrics: {engine.get_metrics()}")
    print("✓ Full observability and performance")
    print()
    return result


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("INTEGRATION ENGINE v2.0.0 MIGRATION DEMONSTRATION")
    print("=" * 60 + "\n")
    
    # Run all migration stages
    v1_style()
    v2_minimal()
    v2_cached()
    v2_full()
    
    print("=" * 60)
    print("MIGRATION COMPLETE")
    print("=" * 60)
