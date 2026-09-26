"""CHME 202 - Week 7 - Midterm practice problems (Weeks 1-6) with computed solutions.

Run without arguments to print the problems; add --solutions to print the answers:
    python w07_midterm_practice.py
    python w07_midterm_practice.py --solutions
Solve by hand first (calculator), then check.
"""

import math
import sys

from fluidmech import Fluid
from fluidmech import laminar as lam
from fluidmech import rheology as rh
from fluidmech.constants import G
from fluidmech.hydrostatics import RotatingTank, accelerating_surface_slope, rectangular_gate
from fluidmech.properties import water_density


def p1():
    stress = [2.1, 3.3, 5.2, 8.3]  # measured shear stress [Pa] at 10, 30, 100, 300 1/s
    fit = rh.fit_power_law([10, 30, 100, 300], stress)
    return (
        f"P1. A rheometer gives tau = {stress} Pa at shear rates 10, 30, 100, 300 1/s. Fit a power-law model and\n"
        "    classify the fluid.",
        f"K = {fit.K:.3f} Pa s^n, n = {fit.n:.3f} -> {fit.behaviour}",
    )


def p2():
    g = rectangular_gate(width=2.0, height=3.0, top_depth=1.5)
    return (
        "P2. A vertical rectangular gate 2 m wide and 3 m high has its top edge 1.5 m below a water surface.\n"
        "    Find the hydrostatic force and the depth of the centre of pressure.",
        f"F = {g.force / 1e3:.1f} kN, centre of pressure at {g.center_of_pressure_depth:.3f} m depth",
    )


def p3():
    slope = accelerating_surface_slope(2.5)
    return (
        "P3. An open tank of water accelerates horizontally at 2.5 m/s2. What angle does the free surface make\n"
        "    with the horizontal?",
        f"tan(theta) = a/g = {-slope:.4f} -> theta = {math.degrees(math.atan(-slope)):.1f} deg",
    )


def p4():
    t = RotatingTank(radius=0.15, initial_depth=0.20, omega=12.0)
    return (
        "P4. A 0.3 m diameter open cylinder holds water 0.20 m deep and rotates at 12 rad/s. Find the depths at\n"
        "    the centre and at the wall, and the speed at which the bottom first becomes exposed.",
        f"centre {t.centre_depth:.4f} m, wall {t.wall_depth:.4f} m, omega = {t.speed_to_expose_bottom():.2f} rad/s",
    )


def p5():
    h = 4.0  # head above the orifice [m]
    v = math.sqrt(2 * G * h)
    q = 0.62 * math.pi * 0.03**2 / 4 * v  # Q = Cd A V for a 30 mm orifice
    return (
        "P5. Water leaves a large open tank through a 30 mm sharp-edged orifice (Cd = 0.62) 4 m below the surface.\n"
        "    Find the jet velocity (ideal) and the discharge.",
        f"V = {v:.2f} m/s, Q = {q * 1000:.2f} L/s",
    )


def p6():
    mu = 0.25  # oil viscosity [Pa s]
    G_ = 2000.0  # -dp/dx [Pa/m] (underscore avoids clashing with gravity G)
    q = lam.plates_flow_rate(0.004, G_, mu)
    tau = lam.plates_wall_shear(0.004, G_, mu)[0]
    return (
        "P6. Oil (mu = 0.25 Pa s) flows between fixed parallel plates 4 mm apart under dp/dx = -2000 Pa/m.\n"
        "    Find the flow rate per metre width, the maximum velocity and the wall shear stress.",
        f"q = {q * 1e4:.3f} cm2/s, u_max = {lam.plates_velocity(0.002, 0.004, G_, mu) * 1000:.2f} mm/s, "
        f"tau_w = {tau:.1f} Pa",
    )


def p7():
    oil = Fluid(900.0, 0.1)
    q = 0.5e-3  # flow [m3/s]
    R = 0.02  # pipe radius [m]
    G_ = lam.pipe_pressure_gradient(q, R, oil.dynamic_viscosity)
    v = q / (math.pi * R**2)
    re = oil.density * v * 2 * R / oil.dynamic_viscosity
    return (
        "P7. Oil (rho = 900 kg/m3, mu = 0.1 Pa s) flows at 0.5 L/s in a 40 mm pipe. Check that the flow is\n"
        "    laminar and find the pressure drop over 25 m and the centreline velocity.",
        f"Re = {re:.0f} (laminar), dp = {G_ * 25 / 1e3:.2f} kPa, u_max = {2 * v:.3f} m/s",
    )


def p8():
    rho = water_density(20)
    dh = 0.12  # manometer reading [m of mercury]
    dp = (13600 - rho) * G * dh  # mercury-under-water manometer
    v = math.sqrt(2 * dp / rho / (1 - 0.5**4))  # Venturi throat velocity, beta = 0.5
    q = v * math.pi * 0.05**2 / 4
    return (
        "P8. A Venturi meter (100 mm inlet, 50 mm throat) in a water line shows a 120 mm mercury-under-water\n"
        "    manometer reading. Find the ideal flow rate.",
        f"dp = {dp / 1e3:.2f} kPa, V_throat = {v:.2f} m/s, Q = {q * 1000:.2f} L/s",
    )


if __name__ == "__main__":
    show = "--solutions" in sys.argv
    for problem in (p1, p2, p3, p4, p5, p6, p7, p8):
        text, answer = problem()
        print(text)
        if show:
            print(f"    ANSWER: {answer}")
        print()
    if not show:
        print("Run with --solutions to see the answers.")
