"""Minimal stub implementations for components not yet fully built.

These allow the OperatorModePipeline and HTTP routes to run end-to-end
in local dev without requiring the full cockpit server, flux engine, or
docs builder to be implemented.

TODO: Replace each stub with a real implementation.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, Optional


class StubCockpitServer:
    """Stub: simulates binding a cockpit WebSocket session."""

    async def bind_runtime(self, run_id: str, layout: Dict[str, Any]) -> str:
        return f"ws_sess_{run_id[:8]}"


class StubFluxEngine:
    """Stub: returns a deterministic flux state derived from graph metrics."""

    def compute_state(
        self,
        layout: Dict[str, Any],
        telemetry_channel: Optional[str] = None,
    ) -> Dict[str, Any]:
        meta = layout.get("meta", {})
        edge_count = int(meta.get("edge_count", 1))
        node_count = int(meta.get("node_count", 1))
        throughput = round(min(1.0, edge_count / max(1, node_count)), 4)
        return {
            "throughput": throughput,
            "phase": round(throughput * 3.14159, 4),
            "coherence": round(0.5 + throughput * 0.4, 4),
            "noise_floor": 0.12,
            "telemetry_channel": telemetry_channel or "",
        }


class StubDocsBuilder:
    """Stub: bundles pipeline artifacts into a serialisable dict."""

    def export_bundle(
        self,
        layout: Dict[str, Any],
        plate71_svg: str,
        flux_state: Dict[str, Any],
        ws_protocol_version: str,
    ) -> Dict[str, Any]:
        return {
            "version": ws_protocol_version,
            "artifacts": {
                "graph_layout": layout.get("meta", {}),
                "plate71_svg_bytes": len(plate71_svg),
                "flux_state": flux_state,
            },
        }
