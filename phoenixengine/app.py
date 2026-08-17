"""PhoenixEngine HTTP application.

Exposes the following endpoints with a zero-dependency stdlib server:

  GET  /api/graph/layout          → tri-layer layout of sample graph
  POST /api/graph/layout          → tri-layer layout of user-supplied graph JSON
  GET  /api/cockpit/handshake     → ready frame for run_id=dev
  POST /api/cockpit/frame         → parse and validate a client frame
  GET  /api/plate71/svg           → Plate71 SVG for sample graph
  POST /api/plate71/svg           → Plate71 SVG for user-supplied layout JSON
  GET  /api/flux/state            → flux state for sample graph
  POST /api/operator/run          → run full OperatorModePipeline (sync wrapper)
  GET  /health                    → {"ok": true}

Run locally:
    python -m phoenixengine.app          # default port 8000
    PORT=9000 python -m phoenixengine.app
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional, Tuple
from urllib.parse import parse_qs, urlparse

from phoenixengine.api.routes_cockpit import handle_handshake, handle_client_frame
from phoenixengine.api.routes_flux import handle_flux_state
from phoenixengine.api.routes_graph import handle_layout, SAMPLE_GRAPH
from phoenixengine.api.routes_plate71 import handle_svg
from phoenixengine.modules.graph_layout.engine import TriLayerDeterministicLayout
from phoenixengine.modules.plate71.svg_builder import Plate71SVGBuilder
from phoenixengine.pipeline.operator_mode import OperatorContext, OperatorModePipeline
from phoenixengine.stubs import StubCockpitServer, StubDocsBuilder, StubFluxEngine


def _build_pipeline() -> OperatorModePipeline:
    return OperatorModePipeline(
        graph_engine=TriLayerDeterministicLayout(),
        cockpit_server=StubCockpitServer(),
        plate71_engine=Plate71SVGBuilder(),
        flux_engine=StubFluxEngine(),
        docs_builder=StubDocsBuilder(),
    )


_PIPELINE = _build_pipeline()


def _run_pipeline_sync(run_id: str, graph_input: Dict[str, Any]) -> OperatorContext:
    ctx = OperatorContext(run_id=run_id, graph_input=graph_input)
    return asyncio.run(_PIPELINE.run(ctx))


class PhoenixHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:  # quieter logging
        print(f"  {self.address_string()} {fmt % args}", file=sys.stderr)

    def _read_json_body(self) -> Optional[Dict[str, Any]]:
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_svg(self, svg: str, status: int = 200) -> None:
        body = svg.encode()
        self.send_response(status)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _not_found(self) -> None:
        self._send_json({"error": "not found"}, 404)

    def do_OPTIONS(self) -> None:  # CORS preflight
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        qs = parse_qs(parsed.query)

        if path == "/health":
            self._send_json({"ok": True})

        elif path == "/api/graph/layout":
            self._send_json(handle_layout())

        elif path == "/api/cockpit/handshake":
            run_id = qs.get("run_id", ["dev"])[0]
            session_id = f"ws_sess_{run_id[:8]}"
            self._send_json(handle_handshake(run_id=run_id, session_id=session_id))

        elif path == "/api/cockpit/ping":
            run_id = qs.get("run_id", ["dev"])[0]
            from phoenixengine.api.routes_cockpit import handle_ping
            self._send_json(handle_ping(run_id=run_id))

        elif path == "/api/plate71/svg":
            layout = handle_layout()
            self._send_svg(handle_svg(layout=layout))

        elif path == "/api/flux/state":
            layout = handle_layout()
            self._send_json(handle_flux_state(layout=layout))

        else:
            self._not_found()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        body = self._read_json_body()

        if path == "/api/graph/layout":
            self._send_json(handle_layout(body))

        elif path == "/api/cockpit/frame":
            if not body:
                self._send_json({"error": "body required"}, 400)
                return
            run_id = body.get("run_id", "dev")
            frame = body.get("frame", {})
            self._send_json(handle_client_frame(run_id=run_id, frame=frame))

        elif path == "/api/plate71/svg":
            layout = body if body else handle_layout()
            self._send_svg(handle_svg(layout=layout))

        elif path == "/api/flux/state":
            layout = body if body else handle_layout()
            self._send_json(handle_flux_state(layout=layout))

        elif path == "/api/operator/run":
            run_id = (body or {}).get("run_id", "dev")
            graph_input = (body or {}).get("graph", SAMPLE_GRAPH)
            ctx = _run_pipeline_sync(run_id=run_id, graph_input=graph_input)
            self._send_json(
                {
                    "run_id": ctx.run_id,
                    "ws_session_id": ctx.ws_session_id,
                    "layout_meta": ctx.layout.get("meta") if ctx.layout else None,
                    "flux_state": ctx.flux_state,
                    "docs_artifacts": ctx.docs_artifacts,
                }
            )

        else:
            self._not_found()


def run(port: int = 8000) -> None:
    server = HTTPServer(("0.0.0.0", port), PhoenixHandler)
    print(f"PhoenixEngine running on http://localhost:{port}", file=sys.stderr)
    print("  GET  /health", file=sys.stderr)
    print("  GET  /api/graph/layout", file=sys.stderr)
    print("  GET  /api/cockpit/handshake", file=sys.stderr)
    print("  GET  /api/plate71/svg", file=sys.stderr)
    print("  GET  /api/flux/state", file=sys.stderr)
    print("  POST /api/operator/run", file=sys.stderr)
    server.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    run(port)
