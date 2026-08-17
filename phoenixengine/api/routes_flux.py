"""Flux state route handler."""
from __future__ import annotations

from typing import Any, Dict

from phoenixengine.stubs import StubFluxEngine

_engine = StubFluxEngine()


def handle_flux_state(layout: Dict[str, Any], telemetry_channel: str = "") -> Dict[str, Any]:
    """Return the current flux state for the given *layout*.

    The state dict is compatible with the ``flux.state`` WebSocket event
    payload and the ``FluxRenderer`` uniform set.
    """
    return _engine.compute_state(layout=layout, telemetry_channel=telemetry_channel)
