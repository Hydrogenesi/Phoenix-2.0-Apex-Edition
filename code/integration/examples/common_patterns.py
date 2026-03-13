#!/usr/bin/env python3
"""
Common Patterns Example — Integration Engine v2.0.0

Demonstrates common integration patterns using the v2.0.0 engine.
"""

from integration_engine import IntegrationEngine

# Initialize engine with caching and telemetry
engine = IntegrationEngine(enable_cache=True, enable_telemetry=True)


def batch_processing():
    """Process multiple pattern batches efficiently"""
    print("=" * 60)
    print("PATTERN 1: Batch Processing")
    print("=" * 60)
    
    pattern_batches = [
        [{"id": f"batch1_{i}", "data": [i, i+1, i+2]} for i in range(3)],
        [{"id": f"batch2_{i}", "data": [i*2, i*2+1, i*2+2]} for i in range(3)],
        [{"id": f"batch3_{i}", "data": [i*3, i*3+1, i*3+2]} for i in range(3)],
    ]
    
    results = []
    for i, batch in enumerate(pattern_batches, 1):
        print(f"Processing batch {i}...")
        result = engine.integrate(batch)
        results.append(result)
    
    print(f"\nProcessed {len(results)} batches")
    print(f"Cache stats: {engine.get_cache_stats()}")
    print(f"Metrics: {engine.get_metrics()}")
    print()


def repeated_integration():
    """Demonstrate cache benefits with repeated patterns"""
    print("=" * 60)
    print("PATTERN 2: Repeated Integration (Cache Benefits)")
    print("=" * 60)
    
    patterns = [
        {"id": "repeat_1", "type": "transformation", "data": [1, 2, 3]},
        {"id": "repeat_2", "type": "harmonic", "data": [4, 5, 6]},
    ]
    
    # First run: cold cache
    print("First integration (cold cache)...")
    result1 = engine.integrate(patterns)
    
    # Subsequent runs: warm cache
    print("Second integration (warm cache)...")
    result2 = engine.integrate(patterns)
    
    print("Third integration (warm cache)...")
    result3 = engine.integrate(patterns)
    
    stats = engine.get_cache_stats()
    print(f"\nCache efficiency:")
    print(f"  Hits: {stats.get('hits', 0)}")
    print(f"  Misses: {stats.get('misses', 0)}")
    print(f"  Hit rate: {stats.get('hit_rate', 0):.1%}")
    print()


def progressive_complexity():
    """Process patterns with increasing complexity"""
    print("=" * 60)
    print("PATTERN 3: Progressive Complexity")
    print("=" * 60)
    
    # Start simple
    simple = [{"id": "simple", "data": [1]}]
    print("Processing simple pattern...")
    engine.integrate(simple)
    
    # Medium complexity
    medium = [{"id": f"medium_{i}", "data": list(range(i*5, i*5+5))} for i in range(3)]
    print("Processing medium complexity...")
    engine.integrate(medium)
    
    # High complexity
    complex_patterns = [
        {"id": f"complex_{i}", "data": list(range(i*10, i*10+10))} 
        for i in range(10)
    ]
    print("Processing high complexity...")
    engine.integrate(complex_patterns)
    
    metrics = engine.get_metrics()
    print(f"\nExecution metrics:")
    print(f"  Total executions: {metrics.get('total_executions', 0)}")
    print(f"  Average duration: {metrics.get('avg_duration', 0):.4f}s")
    print()


def error_handling():
    """Demonstrate error handling and recovery"""
    print("=" * 60)
    print("PATTERN 4: Error Handling")
    print("=" * 60)
    
    try:
        # Valid pattern
        valid = [{"id": "valid", "data": [1, 2, 3]}]
        result = engine.integrate(valid)
        print(f"Valid pattern processed: {result}")
        
        # Note: Actual error handling would depend on implementation
        print("Error rate monitoring available in metrics")
        
    except Exception as e:
        print(f"Error caught: {e}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("COMMON INTEGRATION PATTERNS — DEMONSTRATION")
    print("=" * 60 + "\n")
    
    batch_processing()
    repeated_integration()
    progressive_complexity()
    error_handling()
    
    print("=" * 60)
    print("FINAL STATISTICS")
    print("=" * 60)
    print(f"Cache stats: {engine.get_cache_stats()}")
    print(f"Metrics: {engine.get_metrics()}")
    print()
