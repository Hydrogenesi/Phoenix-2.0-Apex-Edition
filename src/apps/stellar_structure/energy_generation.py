"""Energy Generation — PP chain, CNO, bilateral CNO split"""
import numpy as np
def pp_chain_rate(rho, T): return 1.08e-12*rho*T**4 if T>1e7 else 0.0
def cno_rate(rho, T, X_CNO=0.01): return 8.24e-31*rho*X_CNO*T**18 if T>1.5e7 else 0.0
def bilateral_cno_rate(rho, T, shell_cleared=True):
    if not shell_cleared: return 0.0, False
    rate = cno_rate(rho, T)
    return rate*2.0, rate > 0
def ttauri_gate(rho, T, mass_loss_rate, shell_mass):
    if shell_mass > 0.1: return "SHEDDING", False
    if mass_loss_rate < 1e-9: return "STUCK", False
    return "STABILIZED", True
def total_energy(rho, T, shell_cleared=True):
    pp = pp_chain_rate(rho, T)
    cno, active = bilateral_cno_rate(rho, T, shell_cleared)
    return pp + cno
