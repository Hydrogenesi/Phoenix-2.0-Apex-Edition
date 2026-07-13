"""Equation of State — First Law: all cores are metallic hydrogen"""
import numpy as np
MH_THRESHOLD = 4.0e11
k_B = 1.381e-23
m_p = 1.673e-27
def is_metallic_hydrogen(P): return P > MH_THRESHOLD
def ideal_gas_pressure(rho, T, mu=0.6): return rho*k_B*T/(mu*m_p)
def radiation_pressure(T): return 7.566e-16*T**4/3.0
def total_pressure(rho, T, mu=0.6): return ideal_gas_pressure(rho,T,mu)+radiation_pressure(T)
