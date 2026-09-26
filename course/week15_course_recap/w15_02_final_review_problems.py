"""CHME 202 - Week 15 - Final-exam practice problems (Weeks 9-14) with computed solutions.

python w15_02_final_review_problems.py              # problems only
python w15_02_final_review_problems.py --solutions  # with answers
"""

import sys

from fluidmech import Fluid
from fluidmech import dimensional as dim
from fluidmech import mixing as mx
from fluidmech import pipe_flow as pf
from fluidmech import porous as por
from fluidmech.drag import terminal_velocity

water = Fluid.water(20)


def q1():
    r = pf.head_loss(0.01, 0.1, 300, water, 0.26e-3, 3.5)
    return (
        "Q1. Water at 20 degC flows at 10 L/s through 300 m of 100 mm cast-iron pipe (eps = 0.26 mm) with\n"
        "    fittings totalling K = 3.5. Find Re, f and the total head loss.",
        f"Re = {r.reynolds:.3g}, f = {r.friction_factor:.4f}, h_L = {r.total_head_loss:.2f} m",
    )


def q2():
    q = pf.flow_rate_for_head_loss(15.0, 0.05, 120, water, 0.045e-3)
    return (
        "Q2. What flow rate of water passes through 120 m of 50 mm commercial-steel pipe for a head loss of 15 m?",
        f"Q = {q * 1000:.2f} L/s",
    )


def q3():
    u = terminal_velocity(0.5e-3, 2500, water)
    re = water.density * u * 0.5e-3 / water.dynamic_viscosity
    return (
        "Q3. Find the terminal velocity of a 0.5 mm glass bead (2500 kg/m3) in water at 20 degC. Which regime?",
        f"U_t = {u * 1000:.1f} mm/s, Re = {re:.1f} -> intermediate regime (Stokes law would overpredict)",
    )


def q4():
    dp = por.ergun_pressure_gradient(0.02, 2e-3, 0.4, water.dynamic_viscosity, water.density) * 1.2
    return (
        "Q4. Water flows at a superficial velocity of 2 cm/s through a 1.2 m bed of 2 mm spheres (voidage 0.40).\n"
        "    Find the pressure drop with the Ergun equation.",
        f"dp = {dp / 1e3:.2f} kPa",
    )


def q5():
    groups = dim.pi_groups(
        {
            "dp": "pressure",
            "rho": "density",
            "V": "velocity",
            "d": "diameter",
            "mu": "dynamic_viscosity",
            "sigma": "surface_tension",
        }
    )
    return (
        "Q5. The pressure drop dp across a spray nozzle depends on rho, V, d, mu and sigma. Find the Pi groups\n"
        "    using rho, V, d as repeating variables.",
        "; ".join(dim.format_group(g) for g in groups) + "  (Euler, 1/Re, 1/We)",
    )


def q6():
    tank = mx.StirredTank(1.2, 0.4)
    r = tank.analyse(3.0, 1000, 1e-3)
    return (
        "Q6. A baffled tank (T = 1.2 m, H = T) has a Rushton turbine (D = 0.4 m, Np = 5) at 180 rpm in water.\n"
        "    Find Re, the power, P/V and the 95 % blend time.",
        f"Re = {r['reynolds']:.2e}, P = {r['power_W'] / 1e3:.2f} kW, P/V = {r['power_per_volume_W_m3']:.0f} W/m3, "
        f"theta_95 = {r['blend_time_s']:.1f} s",
    )


if __name__ == "__main__":
    show = "--solutions" in sys.argv
    for q in (q1, q2, q3, q4, q5, q6):
        text, ans = q()
        print(text)
        if show:
            print(f"    ANSWER: {ans}")
        print()
    if not show:
        print("Run with --solutions to see the answers.")
