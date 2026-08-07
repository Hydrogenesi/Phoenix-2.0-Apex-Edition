import pathlib
import sys

import numpy as np
import pytest

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "stellar_structure"))

import phoenix_ignition as ignition
import equation_of_state as eos
from stellar_evolution_refactor import StellarModel


def test_fast_hash_memoizes_by_repr_key():
    ignition._hash_cache.clear()
    state = {"seed": "phoenix", "depth": 1}

    first = ignition.fast_hash(state)
    second = ignition.fast_hash(state)

    assert first == second
    assert len(ignition._hash_cache) == 1


def test_pattern_defaults_to_fast_hash_id():
    ignition._hash_cache.clear()
    pattern = ignition.Pattern(id="", state="Ψ₀")

    assert pattern.id == ignition.fast_hash("Ψ₀")


def test_law_recursion_warns_at_half_depth_threshold():
    pattern = ignition.Pattern(id="warn", state="state", depth=32)
    with pytest.warns(RuntimeWarning, match="warning threshold"):
        ignition.law_recursion(pattern, max_depth=64)


def test_emit_callable_is_lazy_until_log_materialization():
    engine = ignition.PhoenixIgnition(verbose=False)
    calls = {"count": 0}

    def build_message():
        calls["count"] += 1
        return "lazy-message"

    engine._emit(build_message)
    assert calls["count"] == 0

    assert engine.get_log() == ["lazy-message"]
    assert calls["count"] == 1


def test_density_from_pressure_supports_vectorized_inputs():
    model = StellarModel()
    pressures = np.array([1.0e5, 2.5e8, 9.0e10])
    temperatures = np.array([1.0e3, 5.0e5, 1.2e7])

    vectorized = model._density_from_pressure(pressures, temperatures)
    scalar_loop = np.array([
        model._density_from_pressure(float(p), float(t))
        for p, t in zip(pressures, temperatures)
    ])

    np.testing.assert_allclose(vectorized, scalar_loop)


def test_stellar_model_cache_toggle_controls_lru_usage():
    StellarModel._cached_total_energy.cache_clear()

    cached_model = StellarModel(cache_physics=True)
    cached_model._compute_total_energy(1.0e5, 2.0e7)
    cached_model._compute_total_energy(1.0e5, 2.0e7)

    cached_info = StellarModel._cached_total_energy.cache_info()
    assert cached_info.hits >= 1

    StellarModel._cached_total_energy.cache_clear()
    uncached_model = StellarModel(cache_physics=False)
    uncached_model._compute_total_energy(1.0e5, 2.0e7)
    uncached_model._compute_total_energy(1.0e5, 2.0e7)

    uncached_info = StellarModel._cached_total_energy.cache_info()
    assert uncached_info.hits == 0
    assert uncached_info.misses == 0


def test_total_pressure_supports_optional_cache_for_scalar_inputs():
    eos._cached_total_pressure.cache_clear()

    first = eos.total_pressure(1.0e5, 2.0e7, use_cache=True)
    second = eos.total_pressure(1.0e5, 2.0e7, use_cache=True)

    assert first == second
    assert eos._cached_total_pressure.cache_info().hits >= 1
