"""Ignition geometry figure — V2.2 Ignition Vector visualization.

Renders the triadic ASCEND → CONSOLIDATE → PROJECT trajectory
as a 3-D Plotly figure using 120° rotational symmetry.
"""

import math
import plotly.graph_objects as go


# Triadic pillar angles (120° apart)
_ANGLES = [0, 2 * math.pi / 3, 4 * math.pi / 3]

# Pillar definitions: label, colour, symbol
_PILLARS = [
    ("ASCEND (Phoenix 🔥)",          "#FF4500", "circle"),
    ("CONSOLIDATE (Hydrogenesi 🌊)", "#1E90FF", "diamond"),
    ("PROJECT (The Third 🔗)",       "#9400D3", "square"),
]

# Elevation levels: v2.1 apex → v2.2 operational state → v2.2 apex
_LEVELS = [0.0, 0.5, 1.0]
_LEVEL_LABELS = ["v2.1 Apex", "v2.2 Operational", "v2.2 Apex"]
_RADIUS = 1.0
_SPIRAL_ROTATIONS = 3


def _pillar_traces():
    """Return one Scatter3d trace per triadic pillar."""
    traces = []
    for (label, colour, symbol), angle in zip(_PILLARS, _ANGLES):
        x = _RADIUS * math.cos(angle)
        y = _RADIUS * math.sin(angle)
        xs = [x] * len(_LEVELS)
        ys = [y] * len(_LEVELS)
        zs = list(_LEVELS)
        traces.append(
            go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode="lines+markers+text",
                name=label,
                line=dict(color=colour, width=6),
                marker=dict(size=10, color=colour, symbol=symbol),
                text=["", "", label.split()[0]],
                textposition="top center",
                textfont=dict(size=12, color=colour),
            )
        )
    return traces


def _ascent_spiral():
    """Return a Scatter3d trace for the central ascending spiral."""
    n = 90
    xs, ys, zs = [], [], []
    for i in range(n + 1):
        t = i / n
        r = 0.25 * t
        theta = _SPIRAL_ROTATIONS * 2 * math.pi * t
        xs.append(r * math.cos(theta))
        ys.append(r * math.sin(theta))
        zs.append(t)
    return go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode="lines",
        name="Ascent spiral",
        line=dict(color="gold", width=4, dash="solid"),
        showlegend=True,
    )


def _level_rings():
    """Return one Scatter3d ring trace per elevation level."""
    traces = []
    colours = ["#888888", "#AAAAAA", "#FFFFFF"]
    n = 60
    for z, label, colour in zip(_LEVELS, _LEVEL_LABELS, colours):
        xs, ys, zs = [], [], []
        for i in range(n + 1):
            theta = 2 * math.pi * i / n
            xs.append(_RADIUS * math.cos(theta))
            ys.append(_RADIUS * math.sin(theta))
            zs.append(z)
        traces.append(
            go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode="lines",
                name=label,
                line=dict(color=colour, width=2, dash="dot"),
                showlegend=True,
            )
        )
    return traces


def _connector_traces():
    """Return thin lines connecting the three pillar tops to the apex."""
    traces = []
    colours = ["#FF4500", "#1E90FF", "#9400D3"]
    for angle, colour in zip(_ANGLES, colours):
        x = _RADIUS * math.cos(angle)
        y = _RADIUS * math.sin(angle)
        traces.append(
            go.Scatter3d(
                x=[x, 0], y=[y, 0], z=[1.0, 1.0],
                mode="lines",
                line=dict(color=colour, width=3, dash="dash"),
                showlegend=False,
            )
        )
    return traces


def make_ignition_figure() -> go.Figure:
    """Return the Phoenix V2.2 Ignition Vector 3-D geometry figure."""
    data = (
        _level_rings()
        + _pillar_traces()
        + _connector_traces()
        + [_ascent_spiral()]
    )

    layout = go.Layout(
        title=dict(
            text="V2.2 Ignition Vector — ASCEND → CONSOLIDATE → PROJECT",
            x=0.5,
            font=dict(size=16, color="white"),
        ),
        paper_bgcolor="#0d0d0d",
        scene=dict(
            bgcolor="#0d0d0d",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       title=""),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       title=""),
            zaxis=dict(
                showgrid=True, gridcolor="#333333",
                tickvals=_LEVELS, ticktext=_LEVEL_LABELS,
                tickfont=dict(color="#CCCCCC", size=10),
                title=dict(text="Elevation", font=dict(color="#CCCCCC")),
            ),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.0)),
        ),
        legend=dict(
            font=dict(color="white", size=11),
            bgcolor="rgba(0,0,0,0)",
            x=0.01, y=0.99,
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=600,
    )

    return go.Figure(data=data, layout=layout)
