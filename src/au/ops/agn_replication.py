"""AGN Replication Gradient Operator — src.au.ops.agn_replication

Dynamic operator for AGN replication gradient evaluation.  Models an Active
Galactic Nucleus as an accreting black hole and evaluates how its luminosity
pattern replicates across cosmic scales, expressed as a gradient corrected for
cosmological redshift and accretion efficiency.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Eddington luminosity scaling: L_Edd ≈ 1.26 × 10³¹ × (M / M_sun) W
EDDINGTON_FACTOR: float = 1.26e31

# Solar mass (kg)
M_SUN: float = 1.989e30


def _eddington_luminosity(mass_solar: float) -> float:
    """Return the Eddington luminosity (W) for a black hole of *mass_solar* M☉."""
    return EDDINGTON_FACTOR * mass_solar


def _replication_gradient(luminosity: float, redshift: float, eta: float) -> float:
    """Compute the AGN replication gradient.

    Gradient = η · L / (1 + z)²

    The factor (1 + z)² accounts for cosmological dimming; η is the radiative
    accretion efficiency.
    """
    return eta * luminosity / (1.0 + redshift) ** 2


def run(context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute AGN replication gradient evaluation.

    Parameters
    ----------
    context:
        Optional operator context.  Recognised keys:

        * ``mass_solar`` (*float*) – black-hole mass in solar masses
          (default ``1e8``)
        * ``redshift`` (*float*) – AGN redshift z (default ``0.5``)
        * ``eta`` (*float*) – radiative accretion efficiency
          (default ``0.1``)

    Returns
    -------
    dict
        Result dictionary with keys ``operator``, ``kind``, ``inputs``,
        ``eddington_luminosity``, ``replication_gradient``, and ``status``.
    """
    ctx: Dict[str, Any] = context or {}
    mass_solar: float = ctx.get("mass_solar", 1e8)
    redshift: float = ctx.get("redshift", 0.5)
    eta: float = ctx.get("eta", 0.1)

    logger.debug(
        "agn_replication: mass_solar=%.3e  z=%.3f  eta=%.3f",
        mass_solar, redshift, eta,
    )

    luminosity = _eddington_luminosity(mass_solar)
    gradient = _replication_gradient(luminosity, redshift, eta)

    result: Dict[str, Any] = {
        "operator": "agn-replication",
        "kind": "dynamic",
        "inputs": {"mass_solar": mass_solar, "redshift": redshift, "eta": eta},
        "eddington_luminosity": luminosity,
        "replication_gradient": gradient,
        "status": "ok",
    }
    logger.info(
        "agn_replication: L_Edd=%.4e  gradient=%.4e", luminosity, gradient
    )
    return result
