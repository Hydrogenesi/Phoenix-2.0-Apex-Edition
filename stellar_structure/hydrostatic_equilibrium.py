"""
Hydrostatic Equilibrium — Hydrogenesi Framework
dP/dr = -G * M * rho / r^2
dM/dr = 4 * pi * r^2 * rho
"""

import numpy as np

G = 6.674e-11  # gravitational constant

def pressure_gradient(r, M, rho):
    if r < 1e3:
        return 0.0
    return -G * M * rho / r**2

def mass_gradient(r, rho):
    return 4.0 * np.pi * r**2 * rho

def virial_theorem_check(E_grav, E_thermal):
    ratio = abs(E_thermal / E_grav) if E_grav != 0 else 0
    stable = abs(ratio - 0.5) < 0.1
    return stable, ratio

def scale_invariant_binding(M, R, scale='stellar'):
    E_bind = G * M**2 / R
    if scale == 'atomic':
        E_atomic = 13.6 * 1.6e-19
        return E_bind, E_atomic, E_bind / E_atomic
    return E_bind, None, None
