"""HA_8.1 Adapter Operator — src.au.ops.ha_8_1

Adapter operator that normalizes payloads produced by the external HA_8.1
system into the Apex operator contract used across ``src.au.ops`` (a result
dict carrying ``operator``, ``kind``, ``inputs``, ``normalized``, and
``status`` keys, per ``operators/au/registry.yml``).

HA_8.1 is an external component; this module does not embed any of its
internal logic. Instead, it validates the inbound payload shape, records
provenance, and passes the payload through unchanged under a normalized
envelope so that downstream Apex operators (e.g. bridge operators such as
:func:`src.au.ops.q_desic.run`) can consume it uniformly.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Source system identifier recorded on every normalized result.
SOURCE_SYSTEM: str = "HA_8.1"

# Required keys expected on the inbound HA_8.1 payload.
REQUIRED_PAYLOAD_KEYS: tuple = ("payload",)


class HA81AdapterError(ValueError):
    """Raised when an HA_8.1 context is missing required fields."""


def _validate_context(ctx: Dict[str, Any]) -> None:
    """Ensure *ctx* carries the fields required to adapt an HA_8.1 payload."""
    missing = [key for key in REQUIRED_PAYLOAD_KEYS if key not in ctx]
    if missing:
        raise HA81AdapterError(
            f"ha-8-1: missing required context key(s): {', '.join(missing)}"
        )


def _normalize_payload(payload: Any, source_version: str) -> Dict[str, Any]:
    """Wrap the raw HA_8.1 *payload* in the Apex operator envelope."""
    return {
        "source_system": SOURCE_SYSTEM,
        "source_version": source_version,
        "data": payload,
    }


def run(context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute the HA_8.1 adapter operator.

    Parameters
    ----------
    context:
        Optional operator context. Recognised keys:

        * ``payload`` (*Any*) – the raw payload received from HA_8.1
          (required).
        * ``source_version`` (*str*) – HA_8.1 release/version identifier
          (default ``"8.1"``).

    Returns
    -------
    dict
        Result dictionary with keys ``operator``, ``kind``, ``inputs``,
        ``normalized``, and ``status``.

    Raises
    ------
    HA81AdapterError
        If the context does not include a ``payload`` key.
    """
    ctx: Dict[str, Any] = context or {}
    _validate_context(ctx)

    source_version: str = ctx.get("source_version", "8.1")
    payload: Any = ctx["payload"]

    logger.debug(
        "ha_8_1: adapting payload from source_version=%s", source_version,
    )

    normalized = _normalize_payload(payload, source_version)

    result: Dict[str, Any] = {
        "operator": "ha-8-1",
        "kind": "adapter",
        "inputs": {"source_version": source_version},
        "normalized": normalized,
        "status": "ok",
    }
    logger.info("ha_8_1: normalized payload from %s", SOURCE_SYSTEM)
    return result
