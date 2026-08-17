"""
Smoke tests for the end-to-end wiring introduced in this PR.

Validates:
- Graph layout engine produces correct output shape.
- CockpitProtocolV1 handshake + subscribe + ping frames.
- Plate71SVGBuilder renders SVG conforming to the spec contract.
- Flux stub returns expected fields.
- OperatorModePipeline runs end-to-end (all five stages).
- API route handlers are importable and callable.
- app.py can be imported without side-effects.
"""
from __future__ import annotations

import asyncio
import sys
import os

import pytest

# Make the repo root importable when running from the CI working directory.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Graph layout ──────────────────────────────────────────────────────────────

from phoenixengine.modules.graph_layout.engine import TriLayerDeterministicLayout

SAMPLE_GRAPH = {
    "nodes": [
        {"id": "planner-1", "kind": "agent"},
        {"id": "worker-2", "kind": "agent"},
        {"id": "output-1", "kind": "output"},
    ],
    "edges": [
        {"id": "e1", "from": "planner-1", "to": "worker-2", "weight": 0.8},
        {"id": "e2", "from": "worker-2", "to": "output-1", "weight": 1.0},
    ],
}


def test_graph_layout_shape():
    engine = TriLayerDeterministicLayout()
    result = engine.compute_layout(SAMPLE_GRAPH)
    assert result["version"] == "1.0.0"
    assert result["algorithm"] == "tri_layer_deterministic"
    assert len(result["nodes"]) == 3
    assert len(result["edges"]) == 2
    for n in result["nodes"]:
        assert 0.0 <= n["x"] <= 1.0
        assert 0.0 <= n["y"] <= 1.0


def test_graph_layout_deterministic():
    engine = TriLayerDeterministicLayout()
    r1 = engine.compute_layout(SAMPLE_GRAPH)
    r2 = engine.compute_layout(SAMPLE_GRAPH)
    assert r1 == r2


# ── CockpitProtocolV1 ─────────────────────────────────────────────────────────

from phoenixengine.modules.cockpit_ws.protocol import CockpitProtocolV1, ProtocolError


def test_protocol_ready_frame():
    proto = CockpitProtocolV1(run_id="run_test")
    frame = proto.ready_frame(session_id="sess_001")
    assert frame["type"] == "ready"
    assert frame["payload"]["session_id"] == "sess_001"
    assert frame["payload"]["protocol"] == "phoenix.cockpit.v1"


def test_protocol_subscribe():
    proto = CockpitProtocolV1(run_id="run_test")
    client_frame = {
        "v": "1.0.0",
        "type": "subscribe",
        "payload": {"topics": ["graph.snapshot", "flux.state"]},
    }
    result = proto.parse_client_frame(client_frame)
    assert result["action"] == "subscribe"
    assert "graph.snapshot" in proto.subscriptions


def test_protocol_ping_pong():
    proto = CockpitProtocolV1(run_id="run_test")
    ping = proto.ping_frame()
    assert ping["type"] == "ping"
    pong_frame = {"v": "1.0.0", "type": "pong", "payload": {}}
    result = proto.parse_client_frame(pong_frame)
    assert result["action"] == "pong"


def test_protocol_error_on_bad_version():
    proto = CockpitProtocolV1(run_id="run_test")
    with pytest.raises(ProtocolError) as exc_info:
        proto.parse_client_frame({"v": "99.0", "type": "pong", "payload": {}})
    assert exc_info.value.code == "BAD_VERSION"


def test_protocol_error_frame():
    proto = CockpitProtocolV1(run_id="run_test")
    frame = proto.error_frame("RATE_LIMITED", "too many frames", retry_ms=1000)
    assert frame["type"] == "error"
    assert frame["payload"]["code"] == "RATE_LIMITED"
    assert frame["payload"]["retry_ms"] == 1000


# ── Plate71 SVG ──────────────────────────────────────────────────────────────

from phoenixengine.modules.plate71.svg_builder import Plate71SVGBuilder


def _make_layout():
    engine = TriLayerDeterministicLayout()
    return engine.compute_layout(SAMPLE_GRAPH)


def test_plate71_svg_contract():
    builder = Plate71SVGBuilder()
    layout = _make_layout()
    svg = builder.render(layout)
    assert svg.startswith("<svg")
    assert 'data-spec="plate71@1.0.0"' in svg
    assert "plate71-primary_rings" in svg
    assert "plate71-agent_nodes" in svg
    assert "plate71-labels" in svg


def test_plate71_svg_escapes_node_ids():
    layout = {
        "nodes": [{"id": '<script>"xss"</script>', "x": 0.5, "y": 0.5, "kind": "agent"}],
        "edges": [],
    }
    builder = Plate71SVGBuilder()
    svg = builder.render(layout)
    assert "<script>" not in svg


# ── Flux stub ────────────────────────────────────────────────────────────────

from phoenixengine.stubs import StubFluxEngine


def test_flux_stub_fields():
    engine = StubFluxEngine()
    layout = _make_layout()
    state = engine.compute_state(layout=layout, telemetry_channel="ws:sess_001")
    for field in ("throughput", "phase", "coherence", "noise_floor"):
        assert field in state
    assert 0.0 <= state["throughput"] <= 1.0


# ── Full pipeline ─────────────────────────────────────────────────────────────

from phoenixengine.pipeline.operator_mode import OperatorContext, OperatorModePipeline
from phoenixengine.stubs import StubCockpitServer, StubDocsBuilder


def test_operator_pipeline_e2e():
    pipeline = OperatorModePipeline(
        graph_engine=TriLayerDeterministicLayout(),
        cockpit_server=StubCockpitServer(),
        plate71_engine=Plate71SVGBuilder(),
        flux_engine=StubFluxEngine(),
        docs_builder=StubDocsBuilder(),
    )
    ctx = OperatorContext(run_id="test-run", graph_input=SAMPLE_GRAPH)
    result = asyncio.run(pipeline.run(ctx))

    assert result.layout is not None
    assert result.ws_session_id is not None
    assert result.plate71_svg is not None and result.plate71_svg.startswith("<svg")
    assert result.flux_state is not None
    assert result.docs_artifacts is not None


# ── API route handlers ────────────────────────────────────────────────────────

def test_routes_graph_layout():
    from phoenixengine.api.routes_graph import handle_layout
    layout = handle_layout()
    assert "nodes" in layout and "edges" in layout


def test_routes_cockpit_handshake():
    from phoenixengine.api.routes_cockpit import handle_handshake
    frame = handle_handshake(run_id="dev", session_id="ws_sess_dev")
    assert frame["type"] == "ready"


def test_routes_plate71():
    from phoenixengine.api.routes_plate71 import handle_svg
    from phoenixengine.api.routes_graph import handle_layout
    svg = handle_svg(layout=handle_layout())
    assert "<svg" in svg


def test_routes_flux():
    from phoenixengine.api.routes_flux import handle_flux_state
    from phoenixengine.api.routes_graph import handle_layout
    state = handle_flux_state(layout=handle_layout())
    assert "throughput" in state


# ── app.py importable ─────────────────────────────────────────────────────────

def test_app_module_importable():
    import phoenixengine.app as app_module  # noqa: F401
    assert hasattr(app_module, "PhoenixHandler")
    assert hasattr(app_module, "run")
