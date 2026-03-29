"""
integration_engine.py

Production-ready Integration Engine v2.0.0
Implements:
- ThreeFingerWaltz (base)
- CachedThreeFingerWaltz (LRU caching)
- InstrumentedThreeFingerWaltz (telemetry + caching)
- IntegrationEngine (strategy selector + orchestration)
"""

from __future__ import annotations
import logging
import time
from collections import namedtuple, OrderedDict
from typing import Any, Dict, List, Optional, Tuple

# Named tuple compatible with functools.lru_cache's CacheInfo for drop-in compatibility
_CacheInfo = namedtuple("_CacheInfo", ["hits", "misses", "maxsize", "currsize"])


# ------------------------------------------------------------
# 1. Base Waltz
# ------------------------------------------------------------

class ThreeFingerWaltz:
    """
    Minimal, uninstrumented Three-Finger Waltz.
    Performs a direct integration of the provided patterns.
    """

    def __init__(self, patterns: Optional[List[Any]] = None):
        self.patterns: List[Any] = patterns if patterns is not None else []

    def dance(self, patterns: Optional[List[Any]] = None) -> Any:
        """
        Execute the waltz. Override this in subclasses if needed.

        Args:
            patterns: Patterns to integrate. Falls back to self.patterns when omitted.
        """
        # Placeholder logic — replace with your real integration logic.
        actual = patterns if patterns is not None else self.patterns
        return tuple(actual)


# ------------------------------------------------------------
# 2. Cached Waltz
# ------------------------------------------------------------

class CachedThreeFingerWaltz(ThreeFingerWaltz):
    """
    Adds LRU caching to the Three-Finger Waltz.

    The cache persists for the lifetime of this instance, so repeated calls
    with the same patterns benefit from O(1) lookups instead of recomputing.
    """

    def __init__(self, patterns: Optional[List[Any]] = None, cache_size: int = 128):
        super().__init__(patterns)
        self.cache_size = cache_size
        # OrderedDict preserves insertion order for LRU eviction (no extra dependency)
        self._lru: OrderedDict = OrderedDict()
        self._hits = 0
        self._misses = 0

    @staticmethod
    def _make_key(patterns: List[Any]) -> Tuple[Any, ...]:
        """
        Build a hashable cache key from a patterns list.
        Hashable items are used directly; unhashable items fall back to repr().
        """
        key_parts: List[Any] = []
        for p in patterns:
            try:
                hash(p)
                key_parts.append(p)
            except TypeError:
                key_parts.append(repr(p))
        return tuple(key_parts)

    def dance(self, patterns: Optional[List[Any]] = None) -> Any:
        actual = patterns if patterns is not None else self.patterns

        # When cache_size is 0, bypass caching entirely
        if not self.cache_size:
            self._misses += 1
            return super().dance(actual)

        key = self._make_key(actual)

        if key in self._lru:
            self._hits += 1
            self._lru.move_to_end(key)          # mark as most-recently used
            return self._lru[key]

        self._misses += 1
        result = super().dance(actual)           # compute with original patterns
        if len(self._lru) >= self.cache_size:
            self._lru.popitem(last=False)        # evict least-recently-used entry
        self._lru[key] = result
        return result

    def cache_info(self) -> _CacheInfo:
        return _CacheInfo(
            hits=self._hits,
            misses=self._misses,
            maxsize=self.cache_size,
            currsize=len(self._lru),
        )


# ------------------------------------------------------------
# 3. Instrumented Waltz
# ------------------------------------------------------------

class InstrumentedThreeFingerWaltz(CachedThreeFingerWaltz):
    """
    Fully instrumented Three-Finger Waltz.
    Adds:
    - Structured logging
    - Execution metrics
    - Cache visibility
    """

    def __init__(
        self,
        patterns: Optional[List[Any]] = None,
        cache_size: int = 128,
        log_level: int = logging.INFO,
    ):
        super().__init__(patterns, cache_size=cache_size)

        self.logger = logging.getLogger("IntegrationEngine")
        self.logger.setLevel(log_level)

        self.metrics = {
            "total_executions": 0,
            "total_duration": 0.0,
            "error_count": 0,
        }

    def dance(self, patterns: Optional[List[Any]] = None) -> Any:
        actual = patterns if patterns is not None else self.patterns
        start = time.perf_counter()
        self.logger.info(f"[WALTZ] Starting integration of {len(actual)} patterns")

        try:
            result = super().dance(actual)
        except Exception as e:
            self.metrics["error_count"] += 1
            self.logger.error(f"[WALTZ] Error: {e}")
            raise

        duration = time.perf_counter() - start
        self.metrics["total_executions"] += 1
        self.metrics["total_duration"] += duration

        self.logger.info(f"[WALTZ] Completed in {duration:.6f}s")
        return result

    def get_metrics(self) -> Dict[str, Any]:
        n = self.metrics["total_executions"]
        avg = self.metrics["total_duration"] / n if n > 0 else 0.0
        return {
            "total_executions": n,
            "avg_duration_seconds": avg,
            "error_rate": self.metrics["error_count"] / n if n > 0 else 0.0,
        }


# ------------------------------------------------------------
# 4. Integration Engine (Strategy Selector)
# ------------------------------------------------------------

class IntegrationEngine:
    """
    High-level orchestrator that selects the correct waltz implementation
    based on configuration flags.

    Strategy:
        enable_cache + enable_telemetry → InstrumentedThreeFingerWaltz
        enable_cache only              → CachedThreeFingerWaltz
        enable_telemetry only          → InstrumentedThreeFingerWaltz (cache_size=0)
        neither                        → ThreeFingerWaltz

    The waltz instance is created once and reused across all integrate() calls
    so that the LRU cache accumulates hits over the engine's lifetime.
    """

    def __init__(
        self,
        enable_cache: bool = True,
        enable_telemetry: bool = True,
        cache_size: int = 128,
        log_level: int = logging.INFO,
    ):
        self.enable_cache = enable_cache
        self.enable_telemetry = enable_telemetry
        self.cache_size = cache_size
        self.log_level = log_level

        # Create the waltz once so the cache persists across integrate() calls
        self._waltz = self._create_waltz()

    def _create_waltz(self) -> ThreeFingerWaltz:
        if self.enable_cache and self.enable_telemetry:
            return InstrumentedThreeFingerWaltz(
                cache_size=self.cache_size, log_level=self.log_level
            )

        if self.enable_cache:
            return CachedThreeFingerWaltz(cache_size=self.cache_size)

        if self.enable_telemetry:
            return InstrumentedThreeFingerWaltz(
                cache_size=0, log_level=self.log_level
            )

        return ThreeFingerWaltz()

    def integrate(self, patterns: List[Any]) -> Any:
        return self._waltz.dance(patterns)

    def get_cache_stats(self) -> Dict[str, Any]:
        if hasattr(self._waltz, "cache_info"):
            info = self._waltz.cache_info()
            if info.maxsize == 0:
                return {"cache": "disabled"}
            total = info.hits + info.misses
            return {
                "hits": info.hits,
                "misses": info.misses,
                "maxsize": info.maxsize,
                "currsize": info.currsize,
                "hit_rate": info.hits / total if total > 0 else 0.0,
            }
        return {"cache": "disabled"}

    def get_metrics(self) -> Dict[str, Any]:
        if hasattr(self._waltz, "get_metrics"):
            return self._waltz.get_metrics()
        return {"metrics": "disabled"}
