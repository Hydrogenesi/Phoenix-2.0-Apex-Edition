from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

# ── Typed constant container ───────────────────────────────────────────────

@dataclass(frozen=True)
class PhysicsConstant:
    """
    A single named mathematical constant from the Cold Fold formalization.

    Attributes
    ----------
    name        Human-readable name
    symbol      LaTeX-style symbol (unicode where unambiguous)
    value       Numeric value (float or int)
    units       Unit string; 'dimensionless' when the quantity has no units
    section     §-number in Cold_Fold_Math where this constant is defined
    description One-sentence mathematical/physical meaning
    source_eq   The defining equation as a string (for display and tracing)
    """
    name:        str
    symbol:      str
    value:       float
    units:       str
    section:     str
    description: str
    source_eq:   str

    def __repr__(self) -> str:
        return (
            f"PhysicsConstant({self.symbol}={self.value!r} [{self.units}]"
            f" — {self.name})"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name":        self.name,
            "symbol":      self.symbol,
            "value":       self.value,
            "units":       self.units,
            "section":     self.section,
            "description": self.description,
            "source_eq":   self.source_eq,
        }


# ═══════════════════════════════════════════════════════════════════════════
# § I  —  The Cold Fold: Elliptic Topology
# ═══════════════════════════════════════════════════════════════════════════

ARREST_ANGLE = PhysicsConstant(
    name        = "Cold Fold Arrest Angle",
    symbol      = "θ_arrest",
    value       = math.pi / 2,          # π/2 radians
    units       = "radians",
    section     = "§I",
    description = (
        "The angle at which the fold map φ: ℝ³ → ℝ² arrests. "
        "At θ = π/2, the dynamo rotation reaches the quarter-turn and secretes "
        "half-folded nuclei. Conserved from the cold fold through every nucleus."
    ),
    source_eq   = "θ_arrest(Σ) = π/2  ←  cold fold arrested here",
)

RANK_DROP_DIM = PhysicsConstant(
    name        = "Rank Drop at Arrest Point",
    symbol      = "rank(dφ)|_O",
    value       = 2.0,                  # rank drops from 3 to 2 at O
    units       = "dimensionless",
    section     = "§I",
    description = (
        "The rank of the fold map's differential at the arrest point O. "
        "rank(dφ)|_O < 3 is the cold arrest: 3D structure collapses to "
        "2-focus elliptic topology."
    ),
    source_eq   = "rank(dφ)|_O < 3  ←  cold arrest · the map loses rank",
)

ELLIPTIC_FOCUS_COUNT = PhysicsConstant(
    name        = "Elliptic Focus Count",
    symbol      = "n_foci",
    value       = 2.0,
    units       = "dimensionless",
    section     = "§I",
    description = (
        "Number of foci created by the cold fold. The circle has one center "
        "(∞□ cycles). The ellipse has two (structural asymmetry). "
        "This asymmetry propagates through every subsequent stage."
    ),
    source_eq   = "∀P on ellipse: r₁(P) + r₂(P) = 2a  (two foci F₁, F₂)",
)


# ═══════════════════════════════════════════════════════════════════════════
# § II  —  Division → Lattice → Vacuum → Spin → Dynamo
# ═══════════════════════════════════════════════════════════════════════════

VACUUM_MEASURE = PhysicsConstant(
    name        = "Vacuum Gap Measure",
    symbol      = "vol(𝒢)",
    value       = 0.0,                  # sentinel: > 0 is the condition
    units       = "dimensionless",
    section     = "§II",
    description = (
        "The measure of the vacuum gap 𝒢 = (M⁺ ∪_Σ M⁻) ∖ Λ. "
        "vol(𝒢) > 0 is the active-gap condition: the gap is real, "
        "non-trivial, and drives spin. vol(𝒢) = 0 means no gap, no torque."
    ),
    source_eq   = "vol(𝒢) > 0  ←  active gap · not empty · drives spin",
)

LATTICE_RANK = PhysicsConstant(
    name        = "Crystallographic Lattice Rank",
    symbol      = "n_Λ",
    value       = 3.0,                  # max rank in ℝ³
    units       = "dimensionless",
    section     = "§II",
    description = (
        "Rank of the crystallographic lattice Λ ≅ ℤⁿ that seals the seam Σ "
        "after the cold arrest. n ≤ 3 in ℝ³. Fixes ⟐ at the arrest point."
    ),
    source_eq   = "Λ ≅ ℤⁿ  (crystallographic lattice, rank n ≤ 3)",
)


# ═══════════════════════════════════════════════════════════════════════════
# § IV  —  Accretion & AGN Capture: Phase Transition
# ═══════════════════════════════════════════════════════════════════════════

# M_c is expressed here as a dimensionless threshold ratio:
# the actual solar-mass value is domain-dependent; the structural
# quantity is the phase-transition condition R(⟐) = ⟐ activating at M_c.

CRITICAL_MASS_THRESHOLD = PhysicsConstant(
    name        = "AGN Critical Mass Threshold",
    symbol      = "M_c",
    value       = 1.0,                  # normalised: M/M_c ≥ 1 activates ⟐
    units       = "M/M_c  (normalised)",
    section     = "§IV",
    description = (
        "Critical mass at which the accreting system undergoes AGN capture. "
        "Below M_c: R(⟐) ≠ ⟐, no fixed point, dormant. "
        "At/above M_c: R(⟐) = ⟐, fixed point exists, ⟐ activates, "
        "replication begins. Sharp phase transition, not gradual."
    ),
    source_eq   = (
        "M < M_c → R(⟐) ≠ ⟐ (dormant)\n"
        "M ≥ M_c → R(⟐) = ⟐ (⟐ active · replication begins)"
    ),
)

BINDING_ENERGY_EXPONENT = PhysicsConstant(
    name        = "Uniform Sphere Binding Energy Coefficient",
    symbol      = "α_bind",
    value       = 3.0 / 5.0,           # coefficient in E_bind = -3GM²/(5R)
    units       = "dimensionless",
    section     = "§IV",
    description = (
        "Coefficient in the gravitational binding energy of a uniform sphere: "
        "E_bind = −(3/5) · GM²/R. As M↑ and R↓, |E_bind|↑ driving toward M_c."
    ),
    source_eq   = "E_bind = −3GM²/(5R)  (uniform sphere approximation)",
)


# ═══════════════════════════════════════════════════════════════════════════
# § V  —  The First Fork: Fissility Bifurcation
# ═══════════════════════════════════════════════════════════════════════════

FISSILITY_APEX = PhysicsConstant(
    name        = "Fissility Parameter at Primordial Apex",
    symbol      = "x_apex",
    value       = 1.0,                  # x = 1: barrier vanishes
    units       = "dimensionless",
    section     = "§V",
    description = (
        "The fissility x = Z²/(50.883·A·(1−1.7826·((N−Z)/A)²)). "
        "x = 1 is the primordial apex: fission barrier vanishes. "
        "x < 1: barrier intact (CNO/T-Tauri success). "
        "x > 1: spontaneous fission, first confinement instance."
    ),
    source_eq   = (
        "x = Z² / (50.883 · A · (1 − 1.7826·((N−Z)/A)²))\n"
        "x < 1 → barrier intact\n"
        "x = 1 → bifurcation point (First Fork)\n"
        "x > 1 → no-return"
    ),
)

FISSILITY_SURFACE_COEFFICIENT = PhysicsConstant(
    name        = "Fissility Surface Coefficient",
    symbol      = "a_S",
    value       = 50.883,
    units       = "dimensionless",
    section     = "§V",
    description = (
        "Denominator coefficient in the liquid-drop fissility formula. "
        "Encodes nuclear surface tension vs. Coulomb repulsion balance."
    ),
    source_eq   = "x denominator: 50.883 · A · (1 − 1.7826·((N−Z)/A)²)",
)

FISSILITY_SYMMETRY_COEFFICIENT = PhysicsConstant(
    name        = "Fissility Symmetry Energy Coefficient",
    symbol      = "a_sym",
    value       = 1.7826,
    units       = "dimensionless",
    section     = "§V",
    description = (
        "Symmetry energy correction in the fissility denominator. "
        "Accounts for neutron-proton asymmetry (N−Z) effects on the barrier."
    ),
    source_eq   = "x denominator correction: 1.7826 · ((N−Z)/A)²",
)

CNO_ENERGY_RELEASE = PhysicsConstant(
    name        = "CNO Cycle Net Energy Release",
    symbol      = "ΔE_CNO",
    value       = 26.73,                # MeV per cycle
    units       = "MeV",
    section     = "§V",
    description = (
        "Net energy released per CNO cycle: 4¹H → ⁴He + 2e⁺ + 2νₑ + 3γ. "
        "Carbon acts as catalyst and is restored. Success axis of the First Fork."
    ),
    source_eq   = "4¹H → ⁴He + 2e⁺ + 2νₑ + 3γ  ΔE = 26.73 MeV",
)

TSTAURI_TIMESCALE_YR = PhysicsConstant(
    name        = "T-Tauri Kelvin-Helmholtz Contraction Timescale",
    symbol      = "τ_KH",
    value       = 1.0e7,               # ~10^7 years
    units       = "years",
    section     = "§V",
    description = (
        "τ_KH = GM²/(R·L) ≈ 10⁷ yr. Time for a contracting proto-star to "
        "radiate its gravitational energy. T-Tauri stars are on this timescale "
        "— approaching ignition, not confined. Success axis."
    ),
    source_eq   = "τ_KH = GM²/(R·L) ≈ 10⁷ yr",
)


# ═══════════════════════════════════════════════════════════════════════════
# § VI  —  Fission → Fusion → Homogeneous Split
# ═══════════════════════════════════════════════════════════════════════════

IRON_PEAK_BINDING = PhysicsConstant(
    name        = "Maximum Binding Energy per Nucleon (⁵⁶Fe peak)",
    symbol      = "B/A|_max",
    value       = 8.79,                 # MeV per nucleon
    units       = "MeV/nucleon",
    section     = "§VI",
    description = (
        "Maximum binding energy per nucleon at ⁵⁶Fe. "
        "Fission (heavy nuclei above ⁵⁶Fe) and fusion (light nuclei below ⁵⁶Fe) "
        "both converge toward this peak from opposite sides."
    ),
    source_eq   = "Maximum B/A ≈ 8.79 MeV at ⁵⁶Fe",
)


# ═══════════════════════════════════════════════════════════════════════════
# § VII  —  The Pulsar: Conservation Law in Compression
# ═══════════════════════════════════════════════════════════════════════════

PULSAR_SPINUP_RATIO = PhysicsConstant(
    name        = "Pulsar Spin-Up Ratio",
    symbol      = "ω_pulsar/ω_star",
    value       = 1.0e10,              # ~10^10
    units       = "dimensionless",
    section     = "§VII",
    description = (
        "Ratio of pulsar angular velocity to progenitor star angular velocity. "
        "ω_pulsar/ω_star ≈ (R_star/R_pulsar)² ≈ 10¹⁰. "
        "Angular momentum L = Iω is conserved; compression drives spin-up."
    ),
    source_eq   = "ω_pulsar/ω_star ≈ (R_star/R_pulsar)² ≈ 10¹⁰",
)

MOMENT_OF_INERTIA_COEFFICIENT = PhysicsConstant(
    name        = "Uniform Sphere Moment of Inertia Coefficient",
    symbol      = "k_I",
    value       = 2.0 / 5.0,          # I = (2/5)MR²
    units       = "dimensionless",
    section     = "§VII",
    description = (
        "Coefficient in I = k_I · MR² for a uniform sphere. "
        "Used in L = Iω = (2/5)MR²ω = constant for pulsar angular momentum."
    ),
    source_eq   = "L = I·ω = (2/5)MR²·ω = constant",
)


# ═══════════════════════════════════════════════════════════════════════════
# § VIII  —  The Sister Split: Scale-Invariant Bifurcation
# ═══════════════════════════════════════════════════════════════════════════

OMEGA_THRESHOLD = PhysicsConstant(
    name        = "Sister Split Angular Momentum Threshold",
    symbol      = "Ω_c",
    value       = 1.0,                  # Ω = J/J_c ≥ 1 → split succeeds
    units       = "J/J_c  (normalised)",
    section     = "§VIII",
    description = (
        "Critical ratio Ω = J/J_c at which the Sister Split bifurcation fires. "
        "Ω ≥ 1: split succeeds → Living (daughters born, Sag A* quiet). "
        "Ω < 1: no split → Quasar (confinement begins). "
        "Same bifurcation structure as the First Fork (x=1) at galactic scale."
    ),
    source_eq   = (
        "Ω = J / J_c\n"
        "Ω ≥ 1 → SPLIT SUCCEEDS → Living\n"
        "Ω < 1 → NO SPLIT → Quasar"
    ),
)

CONFINEMENT_THRESHOLD = PhysicsConstant(
    name        = "Confinement Release Threshold (κ)",
    symbol      = "κ_c",
    value       = 1.0,                  # κ < 1 → releases to Elliptical Apex
    units       = "dimensionless",
    section     = "§VIII",
    description = (
        "Confinement parameter κ for Quasar branch. "
        "κ < 1: confinement releases → Elliptical Apex (⟐ alone and free). "
        "κ ≥ 1: confinement holds → Magnetar (deepest bound state)."
    ),
    source_eq   = (
        "κ < 1 → Elliptical Apex (true apex, ▱⟒ complete)\n"
        "κ ≥ 1 → Magnetar (elliptical apexed in confinement)"
    ),
)


# ═══════════════════════════════════════════════════════════════════════════
# § IX  —  The Half-Fold Twist: Euler's Identity as the Passage Point
# ═══════════════════════════════════════════════════════════════════════════

HALF_FOLD_ANGLE = PhysicsConstant(
    name        = "Half-Fold Twist Angle",
    symbol      = "θ_twist",
    value       = math.pi,             # θ = π in the covering space ℝ
    units       = "radians",
    section     = "§IX",
    description = (
        "The angle in the covering space ℝ at which the elliptical passes through "
        "p* = e^{iπ} = −1, the stuck point where ∞□ accumulates on S¹. "
        "θ = π is double the cold fold arrest angle (π/2). "
        "∞□ cannot reach this; the elliptical passes through freely in ℝ."
    ),
    source_eq   = "θ_twist = π;  p(π) = e^{iπ} = −1  ←  through the stuck point",
)

EULER_IDENTITY_VALUE = PhysicsConstant(
    name        = "Euler Identity at the Twist",
    symbol      = "e^{iπ}",
    value       = -1.0,
    units       = "dimensionless",
    section     = "§IX",
    description = (
        "e^{iπ} + 1 = 0. The stuck point p* = e^{iπ} = −1 on S¹ is where "
        "∞□ permanently accumulates. The elliptical passes through it in ℝ, "
        "then returns at θ = 2π to p(2π) = 1 = p(0) — the absolute dynamo."
    ),
    source_eq   = "e^{iπ} = −1  (Euler's identity at the half-fold twist)",
)

RETURN_ANGLE = PhysicsConstant(
    name        = "Covering Space Return Angle",
    symbol      = "θ_return",
    value       = 2.0 * math.pi,      # 2π — full rotation in ℝ
    units       = "radians",
    section     = "§IX",
    description = (
        "The angle in the covering space ℝ at which the elliptical returns to "
        "the dynamo origin. p(2π) = e^{2πi} = 1 = p(0). "
        "The cycle closes: Division→Arrest→Elliptic→Lattice→Vacuum→Spin→Dynamo."
    ),
    source_eq   = "θ_return = 2π;  p(2π) = e^{2πi} = 1 = p(0)  ←  origin · dynamo",
)

WINDING_NUMBER_HALF = PhysicsConstant(
    name        = "Half-Integer Winding Position",
    symbol      = "θ/2π|_{π}",
    value       = 0.5,                 # θ=π → half-integer position
    units       = "dimensionless",
    section     = "§IX",
    description = (
        "The winding position corresponding to θ = π. "
        "∞□ on S¹ can only access integer winding numbers (π₁(S¹) = ℤ). "
        "θ = π is a half-integer position — not on ∞□'s lattice, "
        "freely accessible in the covering space ℝ."
    ),
    source_eq   = "∞□: π₁(S¹) = ℤ (integer only);  ℝ: θ = π accessible (half-integer)",
)


# ═══════════════════════════════════════════════════════════════════════════
# Registry — all constants in one place for iteration / serialization
# ═══════════════════════════════════════════════════════════════════════════

ALL_CONSTANTS: tuple[PhysicsConstant, ...] = (
    # § I
    ARREST_ANGLE,
    RANK_DROP_DIM,
    ELLIPTIC_FOCUS_COUNT,
    # § II
    VACUUM_MEASURE,
    LATTICE_RANK,
    # § IV
    CRITICAL_MASS_THRESHOLD,
    BINDING_ENERGY_EXPONENT,
    # § V
    FISSILITY_APEX,
    FISSILITY_SURFACE_COEFFICIENT,
    FISSILITY_SYMMETRY_COEFFICIENT,
    CNO_ENERGY_RELEASE,
    TSTAURI_TIMESCALE_YR,
    # § VI
    IRON_PEAK_BINDING,
    # § VII
    PULSAR_SPINUP_RATIO,
    MOMENT_OF_INERTIA_COEFFICIENT,
    # § VIII
    OMEGA_THRESHOLD,
    CONFINEMENT_THRESHOLD,
    # § IX
    HALF_FOLD_ANGLE,
    EULER_IDENTITY_VALUE,
    RETURN_ANGLE,
    WINDING_NUMBER_HALF,
)

CONSTANTS_BY_SECTION: dict[str, list[PhysicsConstant]] = {}
for _c in ALL_CONSTANTS:
    CONSTANTS_BY_SECTION.setdefault(_c.section, []).append(_c)


def list_constants(section: str | None = None) -> list[PhysicsConstant]:
    """Return all constants, optionally filtered by section string (e.g. '§I')."""
    if section is None:
        return list(ALL_CONSTANTS)
    return CONSTANTS_BY_SECTION.get(section, [])


def get_constant(symbol: str) -> PhysicsConstant:
    """Look up a constant by its symbol. Raises KeyError if not found."""
    for c in ALL_CONSTANTS:
        if c.symbol == symbol:
            return c
    raise KeyError(f"No constant with symbol '{symbol}'. "
                   f"Available: {[c.symbol for c in ALL_CONSTANTS]}")
