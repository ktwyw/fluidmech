"""CHME 202 - Week 13 - Example 1: Buckingham Pi for pipe flow, and why it works.

dp = F(rho, V, D, mu, L, eps): 7 variables, 3 dimensions -> 4 Pi groups.
We (a) find the groups automatically and (b) demonstrate that thousands of
different pipes collapse onto one curve when plotted in Pi groups.
Reading: White, Chapter 5.
"""

import random

from fluidmech import Fluid
from fluidmech import dimensional as dim
from fluidmech import pipe_flow as pf

variables = {
    "dp": "pressure",
    "rho": "density",
    "V": "velocity",
    "D": "diameter",
    "mu": "dynamic_viscosity",
    "L": "length",
    "eps": "roughness",
}
print("Dimensional matrix (rows M, L, T):")
print("        " + "".join(f"{n:>6}" for n in variables))
for i, base in enumerate(("M", "L", "T")):
    print(f"  {base:<5} " + "".join(f"{str(dim.parse_dimension(dim.COMMON[v])[i]):>6}" for v in variables.values()))
r = dim.dimension_matrix_rank(variables)
groups = dim.pi_groups(variables)
print(f"\nn = {len(variables)} variables, rank r = {r} -> {len(variables) - r} Pi groups (repeating: rho, V, D):")
names = ["Euler number (pressure / inertia)", "1 / Reynolds number", "length ratio", "relative roughness"]
for g, meaning in zip(groups, names):
    print(f"  Pi = {dim.format_group(g):<24} {meaning}")
print("So dp / (rho V^2) = f(Re, L/D, eps/D)  - and since dp ~ L:  dp = f(Re, eps/D) (L/D) rho V^2 / 2\n")

# Demonstrate the collapse with random 'experiments'
random.seed(1)
print("Random experiments (different fluids, sizes, speeds) with eps/D = 0.001:")
print(f"{'fluid':>8} {'D [m]':>7} {'V [m/s]':>8} {'dp/L [Pa/m]':>12} {'Re':>9} {'f = 2 dp D/(rho V^2 L)':>23}")
options = [(Fluid.water(20), (0.3, 4.0)), (Fluid.air(20), (2.0, 30.0)), (Fluid(880, 0.02, "oil"), (0.5, 3.0))]
for _ in range(8):  # eight random 'experiments'
    fl, (v_lo, v_hi) = random.choice(options)
    D = random.choice([0.02, 0.05, 0.1, 0.3, 1.0])
    V = random.uniform(v_lo, v_hi)
    res = pf.head_loss(V * pf.area(D), D, 1.0, fl, 0.001 * D)
    f = 2 * res.pressure_drop * D / (fl.density * V**2)  # friction factor from the measured dp over 1 m
    print(f"{fl.name[:8]:>8} {D:>7} {V:>8.3g} {res.pressure_drop:>12.3g} {res.reynolds:>9.3g} {f:>23.4f}")
print("dp/L spans several decades, yet f depends only on Re (and eps/D): the Moody diagram is a Pi-group plot.")
