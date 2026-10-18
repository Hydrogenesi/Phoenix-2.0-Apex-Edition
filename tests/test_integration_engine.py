"""Three-Finger Waltz integration engine and its LRU cache."""
import pytest

from integration_engine import (
    CachedThreeFingerWaltz, IntegrationEngine, InstrumentedThreeFingerWaltz, ThreeFingerWaltz,
)


def test_base_waltz_returns_tuple():
    assert ThreeFingerWaltz([1, 2]).dance() == (1, 2)
    assert ThreeFingerWaltz([1, 2]).dance([3]) == (3,)


def test_cache_hits_and_misses():
    w = CachedThreeFingerWaltz(cache_size=4)
    w.dance([1, 2]); w.dance([1, 2]); w.dance([3])
    info = w.cache_info()
    assert (info.hits, info.misses, info.currsize) == (1, 2, 2)


def test_lru_evicts_least_recently_used():
    w = CachedThreeFingerWaltz(cache_size=2)
    w.dance(["a"]); w.dance(["b"])
    w.dance(["a"])            # 'a' becomes most recent
    w.dance(["c"])            # evicts 'b'
    w.dance(["a"])            # still cached -> hit
    w.dance(["b"])            # evicted -> miss
    assert w.cache_info().hits == 2 and w.cache_info().misses == 4


def test_cache_size_zero_disables_cache():
    w = CachedThreeFingerWaltz(cache_size=0)
    w.dance([1]); w.dance([1])
    assert w.cache_info().hits == 0 and w.cache_info().currsize == 0


def test_unhashable_patterns_are_cached():
    w = CachedThreeFingerWaltz()
    assert w.dance([{"a": 1}]) == ({"a": 1},)
    w.dance([{"a": 1}])
    assert w.cache_info().hits == 1


def test_instrumented_records_metrics():
    w = InstrumentedThreeFingerWaltz()
    w.dance([1]); w.dance([1])
    assert isinstance(w.get_metrics(), dict)


@pytest.mark.parametrize("cache,telemetry", [(True, True), (True, False), (False, True), (False, False)])
def test_engine_configurations_agree(cache, telemetry):
    e = IntegrationEngine(enable_cache=cache, enable_telemetry=telemetry)
    assert e.integrate([1, "x"]) == (1, "x")
    assert isinstance(e.get_cache_stats(), dict) and isinstance(e.get_metrics(), dict)


@pytest.mark.known_defect
@pytest.mark.xfail(reason="unhashable items are keyed by repr(), so the list [1] and the "
                          "string '[1]' share a cache key and the second call gets the wrong result")
def test_cache_keys_do_not_collide():
    w = CachedThreeFingerWaltz()
    w.dance([[1]])
    assert w.dance(["[1]"]) == ("[1]",)
