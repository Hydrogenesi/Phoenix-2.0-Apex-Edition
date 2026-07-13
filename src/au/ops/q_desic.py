"""Q-Desic Bridge Operator — src.au.ops.q_desic

Bridge operator mediating the Curvature-Residue ↔ AGN-Replication coupling.
Invokes both child operators with a shared context, then derives a coupling
coefficient that quantifies how strongly the structural curvature residue and
the dynamic AGN replication gradient are entangled at the current parameter
point.
"""

import logging
from typing import Any, Dict, Optional

from src.au.ops.agn_replication import run as _run_agn
from src.au.ops.curvature_residue import run as _run_curvature

logger = logging.getLogger(__name__)


def _coupling_coefficient(residue: float, gradient: float) -> float:
    """Compute the q-desic coupling coefficient.

    κ_q = |residue| / (1 + |gradient|)

    Normalises the curvature residue against the replication gradient so that
    the coefficient remains bounded when the gradient grows large.
    """
    return abs(residue) / (1.0 + abs(gradient))


def run(context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute the Q-Desic bridge operator.

    Couples ``curvature-residue`` (structural) to ``agn-replication``
    (dynamic) and returns their combined outputs alongside a derived coupling
    coefficient.

    Parameters
    ----------
    context:
        Optional operator context forwarded unchanged to both child operators.
        All keys accepted by :func:`src.au.ops.curvature_residue.run` and
        :func:`src.au.ops.agn_replication.run` are valid here.

    Returns
    -------
    dict
        Bridge result with keys ``operator``, ``kind``,
        ``curvature_residue``, ``agn_replication``,
        ``coupling_coefficient``, and ``status``.
    """
    ctx: Dict[str, Any] = context or {}
    logger.debug("q_desic: initiating bridge with context keys=%s", list(ctx.keys()))

    curvature_result = _run_curvature(ctx)
    agn_result = _run_agn(ctx)

    residue: float = curvature_result["residue"]
    gradient: float = agn_result["replication_gradient"]
    coupling = _coupling_coefficient(residue, gradient)

    result: Dict[str, Any] = {
        "operator": "q-desic",
        "kind": "bridge",
        "curvature_residue": curvature_result,
        "agn_replication": agn_result,
        "coupling_coefficient": coupling,
        "status": "ok",
    }
    logger.info("q_desic: coupling_coefficient=%.6e", coupling)
    return result
