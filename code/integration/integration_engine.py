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
from functools import lru_cache
from typing import Any, Dict, List, Tuple


# ------------------------------------------------------------
# 1. Base Waltz
# ------------------------------------------------------------

class ThreeFingerWaltz:
    """
    Minimal, uninstrumented Three-Finger Waltz.
    Performs a direct integration of the provided patterns.
    """

    def __init__(self, patterns: List[Any]):
        self.patterns = patterns

    def dance(self) -> Any:
        """
        Execute the waltz. Override this in subclasses if needed.
        """
        # Placeholder logic — replace with your real integration logic.
        return tuple(self.patterns)


# ------------------------------------------------------------
# 2. Cached Waltz
# ------------------------------------------------------------

class CachedThreeFingerWaltz(ThreeFingerWaltz):
    """
    Adds LRU caching to the Three-Finger Waltz.
    """

    def __init__(self, patterns: List[Any], cache_size: int = 128):
        super().__init__(patterns)
        self.cache_size = cache_size

        # Wrap the dance() method in an LRU cache
        self._cached_dance = lru_cache(maxsize=cache_size)(self._dance_impl)

    def _dance_impl(self, patterns_key: Tuple[Any, ...]) -> Any:
        return super().dance()

    def dance(self) -> Any:
        key = tuple(self.patterns)
        return self._cached_dance(key)

    def cache_info(self):
        return self._cached_dance.cache_info()


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
        patterns: List[Any],
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

    def dance(self) -> Any:
        start = time.perf_counter()
        self.logger.info(f"[WALTZ] Starting integration of {len(self.patterns)} patterns")

        try:
            result = super().dance()
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
        if self.metrics["total_executions"] == 0:
            avg = 0.0
        else:
            avg = self.metrics["total_duration"] / self.metrics["total_executions"]

        return {
            "total_executions": self.metrics["total_executions"],
            "avg_duration_seconds": avg,
            "error_rate": (
                self.metrics["error_count"] / self.metrics["total_executions"]
                if self.metrics["total_executions"] > 0
                else 0.0
            ),
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

        self._last_waltz = None  # store last instance for metrics/cache access

    def _select_waltz(self, patterns: List[Any]):
        if self.enable_cache and self.enable_telemetry:
            return InstrumentedThreeFingerWaltz(
                patterns, cache_size=self.cache_size, log_level=self.log_level
            )

        if self.enable_cache:
            return CachedThreeFingerWaltz(patterns, cache_size=self.cache_size)

        if self.enable_telemetry:
            return InstrumentedThreeFingerWaltz(
                patterns, cache_size=0, log_level=self.log_level
            )

        return ThreeFingerWaltz(patterns)

    def integrate(self, patterns: List[Any]) -> Any:
        waltz = self._select_waltz(patterns)
        self._last_waltz = waltz
        return waltz.dance()

    def get_cache_stats(self) -> Dict[str, Any]:
        if hasattr(self._last_waltz, "cache_info"):
            return self._last_waltz.cache_info()
        return {"cache": "disabled"}

    def get_metrics(self) -> Dict[str, Any]:
        if hasattr(self._last_waltz, "get_metrics"):
            return self._last_waltz.get_metrics()
        return {"metrics": "disabled"}
