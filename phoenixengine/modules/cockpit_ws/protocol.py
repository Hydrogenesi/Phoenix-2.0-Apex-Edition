from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

PROTOCOL_VERSION = "1.0.0"
SUBPROTOCOL = "phoenix.cockpit.v1"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class Envelope:
    type: str
    run_id: str
    seq: int
    payload: Dict[str, Any]
    v: str = PROTOCOL_VERSION
    ts: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "v": self.v,
            "type": self.type,
            "ts": self.ts or _iso_now(),
            "seq": self.seq,
            "run_id": self.run_id,
            "payload": self.payload,
        }


class ProtocolError(Exception):
    def __init__(self, code: str, message: str, retry_ms: Optional[int] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.retry_ms = retry_ms


class CockpitProtocolV1:
    """Validation + frame construction for phoenix.cockpit.v1."""

    CLIENT_TYPES = {"hello", "subscribe", "ack", "command", "pong"}
    SERVER_TYPES = {
        "ready",
        "graph.snapshot",
        "graph.diff",
        "agent.health",
        "agent.queue",
        "agent.message",
        "plate71.state",
        "flux.state",
        "error",
        "ping",
    }

    def __init__(self, run_id: str):
        self.run_id = run_id
        self._seq = 0
        self._last_acked_seq = 0
        self._subscriptions: set[str] = set()

    def next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def server_frame(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if event_type not in self.SERVER_TYPES:
            raise ProtocolError("INVALID_EVENT", f"unsupported server event type: {event_type}")
        env = Envelope(type=event_type, run_id=self.run_id, seq=self.next_seq(), payload=payload)
        return env.to_dict()

    def parse_client_frame(self, frame: Dict[str, Any]) -> Dict[str, Any]:
        self._validate_envelope(frame)
        t = frame["type"]
        payload = frame.get("payload", {})

        if t == "hello":
            self._require(payload, ["client_id", "capabilities"])
            if not isinstance(payload["capabilities"], list):
                raise ProtocolError("BAD_PAYLOAD", "capabilities must be an array")
            return {"action": "hello", "client_id": payload["client_id"], "capabilities": payload["capabilities"]}

        if t == "subscribe":
            self._require(payload, ["topics"])
            if not isinstance(payload["topics"], list):
                raise ProtocolError("BAD_PAYLOAD", "topics must be an array")
            topics = [str(x) for x in payload["topics"]]
            self._subscriptions.update(topics)
            return {"action": "subscribe", "topics": topics}

        if t == "ack":
            self._require(payload, ["seq"])
            seq = int(payload["seq"])
            if seq < self._last_acked_seq:
                raise ProtocolError("BAD_ACK", "ack sequence regressed")
            self._last_acked_seq = seq
            return {"action": "ack", "seq": seq}

        if t == "command":
            self._require(payload, ["name", "target", "args"])
            return {
                "action": "command",
                "name": str(payload["name"]),
                "target": str(payload["target"]),
                "args": payload.get("args", {}),
            }

        if t == "pong":
            return {"action": "pong"}

        raise ProtocolError("INVALID_EVENT", f"unsupported client event type: {t}")

    def ready_frame(self, session_id: str, heartbeat_ms: int = 15000) -> Dict[str, Any]:
        return self.server_frame(
            "ready",
            {
                "session_id": session_id,
                "heartbeat_ms": heartbeat_ms,
                "protocol": SUBPROTOCOL,
            },
        )

    def ping_frame(self) -> Dict[str, Any]:
        return self.server_frame("ping", {})

    def error_frame(self, code: str, message: str, retry_ms: Optional[int] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"code": code, "message": message}
        if retry_ms is not None:
            payload["retry_ms"] = retry_ms
        return self.server_frame("error", payload)

    @property
    def subscriptions(self) -> List[str]:
        return sorted(self._subscriptions)

    @property
    def last_acked_seq(self) -> int:
        return self._last_acked_seq

    def _validate_envelope(self, frame: Dict[str, Any]) -> None:
        self._require(frame, ["v", "type", "payload"])
        if frame["v"] != PROTOCOL_VERSION:
            raise ProtocolError("BAD_VERSION", f"expected {PROTOCOL_VERSION}, got {frame['v']}")
        if frame["type"] not in self.CLIENT_TYPES:
            raise ProtocolError("INVALID_EVENT", f"unsupported client type: {frame['type']}")

    @staticmethod
    def _require(obj: Dict[str, Any], keys: List[str]) -> None:
        for k in keys:
            if k not in obj:
                raise ProtocolError("MISSING_FIELD", f"missing field: {k}")
