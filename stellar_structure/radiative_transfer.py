"""Radiative Transfer — Kramers opacity, Schwarzschild criterion"""
import numpy as np
def kramers_opacity(rho, T): return 4.34e21*rho*T**-3.5
def electron_scattering_opacity(X=0.7): return 0.2*(1+X)
def total_opacity(rho, T, X=0.7): return kramers_opacity(rho,T)+electron_scattering_opacity(X)
def radiative_gradient(r, L, M, P, T): return -3*total_opacity(1e3,T)*1e3*L/(64*np.pi*5.67e-8*r**2*T**3)
def adiabatic_gradient(gamma=5/3): return (gamma-1)/gamma
def is_convective(rho, T, r, L, M, P): return radiative_gradient(r,L,M,P,T) > adiabatic_gradient()
def em_scale_check(r_stellar, r_atomic=5.3e-11, scale_factor=2.044e21):
    r_predicted = r_atomic*scale_factor
    delta = abs(r_stellar-r_predicted)/r_predicted
    return delta < 0.01
