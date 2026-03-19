"""
Proper stellar boundary conditions using Taylor expansion near r=0.
Fixes the arbitrary M_r = 1e20 starting condition.
"""

import numpy as np

def central_boundary_conditions(r_start, rho_c, T_c, epsilon_c):
    """
    Taylor expansion near r=0:
    M(r) = (4/3) * pi * rho_c * r^3
    P(r) = P_c - (2/3) * pi * G * rho_c^2 * r^2
    L(r) = (4/3) * pi * rho_c * epsilon_c * r^3
    T(r) = T_c - (opacity * rho_c * epsilon_c) / (6 * a * c) * rho_c * r^2
    """
    G = 6.674e-11
    a = 7.566e-16
    c = 3e8

    M_r = (4.0/3.0) * np.pi * rho_c * r_start**3
    P_r = -((2.0/3.0) * np.pi * G * rho_c**2 * r_start**2)
    L_r = (4.0/3.0) * np.pi * rho_c * epsilon_c * r_start**3
    T_r = T_c

    return [P_r, M_r, L_r, T_r]

def surface_conditions():
    """
    At stellar surface: P=0, L=L_total, T=T_eff
    Used to check integration accuracy.
    """
    return {'P': 0.0, 'T_eff': 5778.0}
