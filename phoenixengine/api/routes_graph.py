"""Graph layout API route handler."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from phoenixengine.modules.graph_layout.engine import TriLayerDeterministicLayout

_engine = TriLayerDeterministicLayout()

SAMPLE_GRAPH: Dict[str, Any] = {
    "nodes": [
        {"id": "planner-1", "kind": "agent"},
        {"id": "worker-2", "kind": "agent"},
        {"id": "worker-3", "kind": "agent"},
        {"id": "output-1", "kind": "output"},
    ],
    "edges": [
        {"id": "e1", "from": "planner-1", "to": "worker-2", "weight": 0.8},
        {"id": "e2", "from": "planner-1", "to": "worker-3", "weight": 0.6},
        {"id": "e3", "from": "worker-2", "to": "output-1", "weight": 1.0},
        {"id": "e4", "from": "worker-3", "to": "output-1", "weight": 0.9},
    ],
}


def handle_layout(body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Compute and return graph layout.

    Args:
        body: Optional graph dict with ``nodes`` and ``edges``.
              Falls back to :data:`SAMPLE_GRAPH` when ``None``.

    Returns:
        Layout dict produced by :class:`TriLayerDeterministicLayout`.
    """
    graph = body if body else SAMPLE_GRAPH
    return _engine.compute_layout(graph)
