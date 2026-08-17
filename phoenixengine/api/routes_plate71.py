"""Plate71 SVG generation route handler."""
from __future__ import annotations

from typing import Any, Dict, Optional

from phoenixengine.modules.plate71.svg_builder import Plate71SVGBuilder

_builder = Plate71SVGBuilder()


def handle_svg(layout: Dict[str, Any], telemetry: Optional[Dict[str, Any]] = None) -> str:
    """Render a Plate71 SVG for *layout* with optional *telemetry* overlay.

    Returns:
        SVG string conforming to the plate71@1.0.0 spec.
    """
    return _builder.render(layout=layout, telemetry=telemetry or {})
