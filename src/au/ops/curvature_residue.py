"""Curvature Residue Operator — src.au.ops.curvature_residue

Structural operator for curvature residue evaluation.  Computes the Ricci
scalar residue (observed curvature minus the stress-energy contribution plus
the cosmological constant term) and projects it through the Hydrogenesi scale
factor to the cosmic domain.
"""

import logging
import math
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Hydrogenesi scale factor: moon radius / proton radius
SCALE_FACTOR: float = 2.044e21

# Bohr radius (m)
BOHR_RADIUS: float = 5.29177e-11

# Gravitational constant (m³ kg⁻¹ s⁻²)
G: float = 6.674e-11

# Speed of light (m s⁻¹)
C: float = 2.998e8


def _ricci_residue(kappa: float, rho: float, lambda_c: float) -> float:
    """Compute R − (8πG/c²)ρ + Λ (linearised Ricci residue)."""
    stress_energy = (8.0 * math.pi * G / C ** 2) * rho
    return kappa - stress_energy + lambda_c


def _scaled_residue(residue: float, scale: float) -> float:
    """Project residue through the Hydrogenesi scaling (Bohr radius × scale)²."""
    return residue * (BOHR_RADIUS * scale) ** 2


def run(context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute curvature residue evaluation.

    Parameters
    ----------
    context:
        Optional operator context.  Recognised keys:

        * ``kappa`` (*float*) – local curvature scalar (default ``1.0``)
        * ``rho`` (*float*) – energy density in kg m⁻³ (default ``1e-26``)
        * ``lambda_c`` (*float*) – cosmological constant contribution
          (default ``1.19e-52``)
        * ``scale`` (*float*) – override for the Hydrogenesi scale factor

    Returns
    -------
    dict
        Result dictionary with keys ``operator``, ``kind``, ``inputs``,
        ``residue``, ``scaled_residue``, ``scale_factor``, and ``status``.
    """
    ctx: Dict[str, Any] = context or {}
    kappa: float = ctx.get("kappa", 1.0)
    rho: float = ctx.get("rho", 1e-26)
    lambda_c: float = ctx.get("lambda_c", 1.19e-52)
    scale: float = ctx.get("scale", SCALE_FACTOR)

    logger.debug(
        "curvature_residue: kappa=%.4e  rho=%.4e  lambda_c=%.4e",
        kappa, rho, lambda_c,
    )

    residue = _ricci_residue(kappa, rho, lambda_c)
    scaled = _scaled_residue(residue, scale)

    result: Dict[str, Any] = {
        "operator": "curvature-residue",
        "kind": "structural",
        "inputs": {"kappa": kappa, "rho": rho, "lambda_c": lambda_c},
        "residue": residue,
        "scaled_residue": scaled,
        "scale_factor": scale,
        "status": "ok",
    }
    logger.info("curvature_residue: residue=%.6e  scaled=%.6e", residue, scaled)
    return result
