from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Any


@dataclass(frozen=True)
class Node:
    id: str
    kind: str = "agent"


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    weight: float = 1.0


class TriLayerDeterministicLayout:
    """
    Deterministic tri-layer layout:
      - layer 0: sources (in_degree == 0)
      - layer 2: sinks (out_degree == 0)
      - layer 1: middle (all others)

    Within each layer, ordering is deterministic by a stable score and node id.
    Coordinates are normalized into [0, 1].
    """

    def compute_layout(self, graph: Dict[str, Any]) -> Dict[str, Any]:
        nodes = [Node(**n) for n in graph.get("nodes", [])]
        edges = [
            Edge(
                id=e.get("id", f"{e['from']}->{e['to']}"),
                source=e.get("from") or e.get("source"),
                target=e.get("to") or e.get("target"),
                weight=float(e.get("weight", 1.0)),
            )
            for e in graph.get("edges", [])
        ]

        node_ids = [n.id for n in nodes]
        in_deg = {nid: 0 for nid in node_ids}
        out_deg = {nid: 0 for nid in node_ids}
        in_w = {nid: 0.0 for nid in node_ids}
        out_w = {nid: 0.0 for nid in node_ids}

        for e in edges:
            if e.source in out_deg and e.target in in_deg:
                out_deg[e.source] += 1
                in_deg[e.target] += 1
                out_w[e.source] += e.weight
                in_w[e.target] += e.weight

        layer0, layer1, layer2 = [], [], []
        for nid in sorted(node_ids):
            if in_deg[nid] == 0 and out_deg[nid] > 0:
                layer0.append(nid)
            elif out_deg[nid] == 0 and in_deg[nid] > 0:
                layer2.append(nid)
            else:
                layer1.append(nid)

        def sort_layer(nids: List[str], kind: str) -> List[str]:
            if kind == "source":
                return sorted(nids, key=lambda n: (-out_w[n], -out_deg[n], n))
            if kind == "sink":
                return sorted(nids, key=lambda n: (-in_w[n], -in_deg[n], n))
            return sorted(nids, key=lambda n: (-(in_w[n] + out_w[n]), -(in_deg[n] + out_deg[n]), n))

        layer0 = sort_layer(layer0, "source")
        layer1 = sort_layer(layer1, "middle")
        layer2 = sort_layer(layer2, "sink")

        layers = [layer0, layer1, layer2]
        x_positions = [0.15, 0.5, 0.85]

        positioned_nodes = []
        for li, layer in enumerate(layers):
            count = len(layer)
            if count == 0:
                continue
            for idx, nid in enumerate(layer):
                y = (idx + 1) / (count + 1)
                positioned_nodes.append(
                    {
                        "id": nid,
                        "kind": next((n.kind for n in nodes if n.id == nid), "agent"),
                        "x": round(x_positions[li], 6),
                        "y": round(y, 6),
                        "layer": li,
                    }
                )

        edge_out = []
        for e in edges:
            edge_out.append(
                {
                    "id": e.id,
                    "from": e.source,
                    "to": e.target,
                    "weight": e.weight,
                }
            )

        return {
            "version": "1.0.0",
            "algorithm": "tri_layer_deterministic",
            "nodes": positioned_nodes,
            "edges": edge_out,
            "meta": {
                "layer_counts": [len(layer0), len(layer1), len(layer2)],
                "node_count": len(nodes),
                "edge_count": len(edges),
            },
        }
