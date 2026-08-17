from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class OperatorContext:
    run_id: str
    graph_input: Dict[str, Any]
    ws_session_id: Optional[str] = None
    layout: Optional[Dict[str, Any]] = None
    plate71_svg: Optional[str] = None
    flux_state: Optional[Dict[str, Any]] = None
    docs_artifacts: Optional[Dict[str, Any]] = None


class OperatorModePipeline:
    """Runnable orchestrator linking all five modules in strict order."""

    def __init__(self, graph_engine, cockpit_server, plate71_engine, flux_engine, docs_builder):
        self.graph_engine = graph_engine
        self.cockpit_server = cockpit_server
        self.plate71_engine = plate71_engine
        self.flux_engine = flux_engine
        self.docs_builder = docs_builder

    async def run(self, ctx: OperatorContext) -> OperatorContext:
        # 1) MAG auto-layout
        ctx.layout = self.graph_engine.compute_layout(ctx.graph_input)

        # 2) Runtime-bound cockpit websocket session
        ctx.ws_session_id = await self.cockpit_server.bind_runtime(run_id=ctx.run_id, layout=ctx.layout)

        # 3) Plate 71 symbolic layer
        ctx.plate71_svg = self.plate71_engine.render(layout=ctx.layout, telemetry={})

        # 4) Quantum Flux model state
        ctx.flux_state = self.flux_engine.compute_state(layout=ctx.layout, telemetry_channel=f"ws:{ctx.ws_session_id}")

        # 5) Docs export bundle
        ctx.docs_artifacts = self.docs_builder.export_bundle(
            layout=ctx.layout,
            plate71_svg=ctx.plate71_svg,
            flux_state=ctx.flux_state,
            ws_protocol_version="1.0.0",
        )

        return ctx
