"""Cockpit WebSocket protocol route handler."""
from __future__ import annotations

from typing import Any, Dict

from phoenixengine.modules.cockpit_ws.protocol import CockpitProtocolV1, ProtocolError


def make_session(run_id: str) -> CockpitProtocolV1:
    """Create a fresh protocol session for *run_id*."""
    return CockpitProtocolV1(run_id=run_id)


def handle_handshake(run_id: str, session_id: str) -> Dict[str, Any]:
    """Return the ``ready`` frame for a new cockpit connection."""
    proto = make_session(run_id)
    return proto.ready_frame(session_id=session_id)


def handle_client_frame(run_id: str, frame: Dict[str, Any]) -> Dict[str, Any]:
    """Parse *frame* from the client and return a response dict.

    Returns an error frame on protocol violations.
    """
    proto = make_session(run_id)
    try:
        result = proto.parse_client_frame(frame)
        return {"ok": True, "action": result.get("action")}
    except ProtocolError as exc:
        return proto.error_frame(exc.code, exc.message, exc.retry_ms)


def handle_ping(run_id: str) -> Dict[str, Any]:
    """Return a ping frame."""
    proto = make_session(run_id)
    return proto.ping_frame()
