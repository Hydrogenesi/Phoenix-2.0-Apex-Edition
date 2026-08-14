# HA-8 Canonical Statement

Let phi_star be the equilibrium configuration obtained from the HA-8 structural equations.

1. Formal fixed point: E_eq(phi_star) = phi_star
2. Slow-manifold evolution: E_phys(phi_star) != phi_star
3. Octave is symbolic decomposition, not contraction. lambda ~ 0.9999, ~3x10^4 steps for 10^-3 accuracy.
4. Virial equilibrium: 2T(phi_star) + Omega(phi_star) = 0, dynamically stable on V.
5. Constrained positivity: delta^2 F >= c ||(delta_rho, delta_X)||^2 on V, for some c > 0.
   A full proof is left to future work. This is a structural assumption of HA-8.

The HA-8 equilibrium is: a formal fixed point of E_eq, a slow-manifold state under E_phys,
virial-balanced, dynamically stable on V, and approached through an 8-phase structural octave.
