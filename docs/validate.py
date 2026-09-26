"""Compare fluidmech against published reference values and exact solutions.

Usage:  python docs/validate.py        (rewrites docs/VALIDATION.md)
"""

import math
from pathlib import Path

from fluidmech import (
    Fluid,
    Network,
    compressible,
    drag,
    laminar,
    mixing,
    open_channel,
    pipe_flow,
    potential_flow,
    properties,
    turbulence,
)
from fluidmech.constants import G

CASES = []


def case(group, quantity, reference, computed, source, tol=0.01):
    CASES.append((group, quantity, reference, computed, source, tol))


# --- Properties ---------------------------------------------------------------
case("Properties", "Water density at 20 degC [kg/m3]", 998.21, properties.water_density(20), "NIST / IAPWS-95", 0.001)
case(
    "Properties",
    "Water viscosity at 20 degC [mPa s]",
    1.0016,
    properties.water_dynamic_viscosity(20) * 1e3,
    "NIST / IAPWS 2008",
    0.01,
)
case(
    "Properties",
    "Water viscosity at 80 degC [mPa s]",
    0.3544,
    properties.water_dynamic_viscosity(80) * 1e3,
    "NIST / IAPWS 2008",
    0.02,
)
case(
    "Properties",
    "Water vapour pressure at 20 degC [kPa]",
    2.339,
    properties.water_vapor_pressure(20) / 1e3,
    "IAPWS-IF97 steam tables",
    0.01,
)
case(
    "Properties",
    "Water vapour pressure at 100 degC [kPa]",
    101.42,
    properties.water_vapor_pressure(100) / 1e3,
    "IAPWS-IF97 steam tables",
    0.01,
)
case(
    "Properties",
    "Water surface tension at 20 degC [mN/m]",
    72.74,
    properties.water_surface_tension(20) * 1e3,
    "IAPWS 2014",
    0.005,
)
case("Properties", "Air density at 15 degC, 1 atm [kg/m3]", 1.2250, properties.air_density(15), "ISA sea level", 0.001)
case(
    "Properties",
    "Air viscosity at 15 degC [uPa s]",
    17.894,
    properties.air_dynamic_viscosity(15) * 1e6,
    "ISA sea level",
    0.005,
)
case("Properties", "Speed of sound at 15 degC [m/s]", 340.29, compressible.speed_of_sound(15), "ISA sea level", 0.001)

# --- Pipe flow ----------------------------------------------------------------
case("Pipe flow", "Laminar f at Re = 1000", 0.064, pipe_flow.friction_factor(1000), "exact, f = 64/Re", 1e-9)
oil = Fluid(900.0, 0.3)
r = pipe_flow.head_loss(1e-3, 0.05, 10.0, oil)
exact_dp = 128 * 0.3 * 10.0 * 1e-3 / (math.pi * 0.05**4)
case("Pipe flow", "Laminar pressure drop [Pa]", exact_dp, r.pressure_drop, "exact Hagen-Poiseuille", 1e-6)


def prandtl_smooth(re: float) -> float:
    """Prandtl's universal law for smooth pipes, 1/sqrt(f) = 2 log10(Re sqrt(f)) - 0.8, solved independently."""
    x = 8.0
    for _ in range(100):
        x = 2.0 * math.log10(re / x) - 0.8
    return 1.0 / x**2


for re in (1e4, 1e5, 1e6, 1e7):
    case(
        "Pipe flow",
        f"Smooth-pipe f at Re = {re:.0e}",
        prandtl_smooth(re),
        pipe_flow.colebrook(re, 0.0),
        "Prandtl smooth-pipe law",
        0.005,
    )
for rr in (1e-3, 1e-2):
    exact = (2.0 * math.log10(3.7 / rr)) ** -2
    case(
        "Pipe flow",
        f"Fully rough f at eps/D = {rr:g}",
        exact,
        pipe_flow.colebrook(1e12, rr),
        "von Karman rough-pipe law (exact)",
        0.001,
    )
for re, rr, ref in [(1e6, 1e-4, 0.0134), (1e7, 1e-3, 0.0197)]:
    case(
        "Pipe flow",
        f"f at Re = {re:.0e}, eps/D = {rr:g}",
        ref,
        pipe_flow.colebrook(re, rr),
        "Moody (1944) chart, graphical reading",
        0.02,
    )

# --- Networks -----------------------------------------------------------------
net = Network(Fluid.water(20))
net.add_reservoir("R1", 100.0)
net.add_reservoir("R2", 80.0)
net.add_pipe("P", "R1", "R2", 1000.0, 0.2, 0.045e-3, k_minor=1.5)
ref_q = pipe_flow.flow_rate_for_head_loss(20.0, 0.2, 1000.0, Fluid.water(20), 0.045e-3, 1.5)
case(
    "Networks",
    "Single pipe between reservoirs [L/s]",
    ref_q * 1000,
    net.solve().flows["P"] * 1000,
    "direct Type-2 solution",
    1e-6,
)

# --- Open channels ------------------------------------------------------------
ch = open_channel.RectangularChannel(4.0)
yc_exact = (10.0 / 4.0) ** (2 / 3) / G ** (1 / 3)
case("Open channel", "Critical depth, rectangular [m]", yc_exact, ch.critical_depth(10.0), "exact (q^2/g)^(1/3)", 1e-8)
case(
    "Open channel",
    "Minimum specific energy / y_c",
    1.5,
    ch.specific_energy(yc_exact, 10.0) / yc_exact,
    "exact, E_min = 1.5 y_c",
    1e-9,
)
case(
    "Open channel",
    "Sequent depth ratio at Fr1 = 3",
    0.5 * (math.sqrt(73) - 1),
    open_channel.hydraulic_jump_depth(1.0, 3.0),
    "exact Belanger equation",
    1e-12,
)
wide = open_channel.RectangularChannel(1000.0)
yn = wide.normal_depth(1000.0, 0.02, 0.001)
case(
    "Open channel",
    "Normal depth, very wide channel [m]",
    (0.02 / 0.001**0.5) ** 0.6,
    yn,
    "wide-channel limit y = (q n / S^0.5)^0.6",
    0.003,
)

# --- Compressible flow ---------------------------------------------------------
for m, pr, ar in [(0.5, 0.8430, 1.3398), (2.0, 0.1278, 1.6875), (3.0, 0.02722, 4.2346)]:
    case("Compressible", f"p/p0 at M = {m}", pr, compressible.pressure_ratio(m), "NACA 1135 isentropic tables", 0.001)
    case("Compressible", f"A/A* at M = {m}", ar, compressible.area_ratio(m), "NACA 1135 isentropic tables", 0.001)
for m1, m2, p0r in [(1.5, 0.7011, 0.9298), (2.0, 0.5774, 0.7209), (3.0, 0.4752, 0.3283)]:
    s = compressible.normal_shock(m1)
    case("Compressible", f"Shock M2 at M1 = {m1}", m2, s.mach2, "NACA 1135 normal-shock tables", 0.001)
    case(
        "Compressible",
        f"Shock p02/p01 at M1 = {m1}",
        p0r,
        s.stagnation_pressure_ratio,
        "NACA 1135 normal-shock tables",
        0.001,
    )
case(
    "Compressible", "Critical pressure ratio p*/p0", 0.5283, compressible.critical_pressure_ratio(), "NACA 1135", 0.001
)

# --- External flow -------------------------------------------------------------
water = Fluid.water(20)
case(
    "External flow",
    "Terminal velocity, 10 um sand [mm/s]",
    drag.stokes_velocity(10e-6, 2650, water) * 1000,
    drag.terminal_velocity(10e-6, 2650, water) * 1000,
    "Stokes' law (Re << 1)",
    0.02,
)
for re, cd in [(1.0, 27.0), (100.0, 1.09), (1e4, 0.41)]:
    case(
        "External flow",
        f"Sphere Cd at Re = {re:g}",
        cd,
        drag.sphere_drag_coefficient(re),
        "standard drag curve (Clift, Grace & Weber 1978)",
        0.05,
    )
case(
    "External flow",
    "Laminar flat-plate Cf at Re = 1e5",
    1.328 / math.sqrt(1e5),
    drag.flat_plate_friction_coefficient(1e5),
    "exact Blasius solution",
    1e-9,
)


# --- Laminar (exact Navier-Stokes) solutions ----------------------------------
case("Laminar flow", "Square duct f*Re", 56.91, laminar.rectangular_duct_fre(1.0), "Shah & London (1978) exact", 0.001)
case("Laminar flow", "Parallel plates f*Re", 96.0, laminar.rectangular_duct_fre(0.0), "exact", 1e-9)
case("Laminar flow", "Concentric annulus f*Re, k = 0.5", 95.25, laminar.annulus_fre(0.5), "Shah & London (1978)", 0.001)
case(
    "Laminar flow",
    "Power-law pipe, n = 1 -> Hagen-Poiseuille [L/s]",
    laminar.pipe_flow_rate(100.0, 0.01, 1e-3) * 1e3,
    laminar.power_law_pipe_flow_rate(100.0, 0.01, 1e-3, 1.0) * 1e3,
    "exact limit",
    1e-9,
)
film_d = laminar.film_thickness(0.05, 1000.0, 1e-3)
case(
    "Laminar flow",
    "Falling film surface/mean velocity",
    1.5,
    laminar.film_velocity(film_d, film_d, 1000.0, 1e-3) / (0.05 / (1000.0 * film_d)),
    "exact (Nusselt)",
    1e-9,
)

# --- Potential flow -------------------------------------------------------------
cyl = potential_flow.cylinder(10.0, 1.0)
case("Potential flow", "Cylinder Cp at the shoulder", -3.0, cyl.pressure_coefficient(0.0, 1.0, 10.0), "exact", 1e-9)
hb = potential_flow.rankine_half_body(5.0, 10.0)
theta = math.radians(63.0)
r_s = 10.0 * (math.pi - theta) / (2 * math.pi * 5.0 * math.sin(theta))
case(
    "Potential flow",
    "Rankine half-body max surface speed / U",
    1.26,
    hb.speed(r_s * math.cos(theta), r_s * math.sin(theta)) / 5.0,
    "White, Section 8.3",
    0.005,
)

# --- Turbulence -------------------------------------------------------------------
case(
    "Turbulence",
    "Law of the wall u+ at y+ = 1000",
    21.85,
    turbulence.law_of_the_wall(1000.0),
    "log law, kappa = 0.41, B = 5.0",
    0.001,
)
case("Turbulence", "1/7 power law V/U_max", 49 / 60, turbulence.mean_to_max_velocity_ratio(7.0), "exact", 1e-9)

# --- Atmosphere --------------------------------------------------------------------
t11, p11, _ = properties.standard_atmosphere(11000.0)
case("Properties", "ISA pressure at 11 km [Pa]", 22632.1, p11, "ISA / US Standard Atmosphere 1976", 0.001)
case("Properties", "ISA temperature at 11 km [K]", 216.65, t11 + 273.15, "ISA", 1e-6)

# --- Mixing and reactors -------------------------------------------------------------
x = 1.0
a = x / 2
e1 = -0.5772156649 - math.log(a) + sum((-1) ** (k + 1) * a**k / (k * math.factorial(k)) for k in range(1, 30))
lfr_exact = 1.0 - ((1 - a) * math.exp(-a) + a * a * e1)
case(
    "Mixing",
    "Laminar-flow reactor conversion, k tau = 1",
    lfr_exact,
    mixing.laminar_flow_reactor_conversion(x),
    "exact (exponential integral)",
    1e-4,
)
case(
    "Mixing",
    "Tanks in series, N = 5000 -> PFR",
    mixing.pfr_conversion(2.0),
    mixing.tanks_in_series_conversion(2.0, 5000),
    "exact limit",
    1e-3,
)


# --- Advanced topics --------------------------------------------------------------
from fluidmech import cavitation, transients  # noqa: E402

bl = laminar.blasius()
case("Advanced", "Blasius wall shear f''(0)", 0.33206, bl["fpp0"], "Blasius (1908) / Howarth (1938)", 1e-4)
case("Advanced", "Blasius delta_99 / (x Re_x^-1/2)", 4.91, bl["delta99"], "Blasius solution", 0.005)
case("Advanced", "Blasius displacement thickness", 1.7208, bl["delta_star"], "Blasius solution", 0.001)
case("Advanced", "Blasius momentum thickness", 0.6641, bl["theta"], "Blasius solution", 0.001)
moc = transients.moc_valve_closure(600, 0.5, 1200, 0.0, 1.5, 100, closure_time=0.1, t_end=1.0)
case(
    "Advanced",
    "MOC surge, frictionless rapid closure [m]",
    1200 * 1.5 / G,
    max(moc["head_valve"]) - 100.0,
    "Joukowsky dH = c V / g",
    0.01,
)
rp = cavitation.rayleigh_plesset(1e-3, 1e5 + 2.34e3, 2e-4, viscosity=0.0, surface_tension=0.0)
case(
    "Advanced",
    "Empty-cavity collapse time [us]",
    cavitation.rayleigh_collapse_time(1e-3, 998.0, 1e5) * 1e6,
    rp["t"][-1] * 1e6,
    "Rayleigh (1917)",
    1e-3,
)
try:
    import numpy as np  # noqa: E402

    from fluidmech import cfd  # noqa: E402

    cav = cfd.lid_driven_cavity(65, 100.0)
    uc = cav["u"][:, 32]
    case("Advanced", "Cavity Re=100: min centreline u", -0.21090, float(uc.min()), "Ghia, Ghia & Shin (1982)", 0.01)
    case(
        "Advanced",
        "Cavity Re=100: primary vortex psi_min",
        -0.103423,
        float(cav["psi"].min()),
        "Ghia, Ghia & Shin (1982)",
        0.01,
    )
    ks = []
    for seed in (1, 2, 3):
        td = cfd.taylor_dispersion(peclet=20, particles=4000, t_end=6, snapshot_times=(), seed=seed)
        late = td["time"] > 2
        ks.append(np.polyfit(td["time"][late], td["variance"][late], 1)[0] / 2)
    case(
        "Advanced",
        "Taylor dispersion D_eff/D at Pe = 20",
        td["theory_K"],
        float(np.mean(ks)),
        "Taylor (1953), Aris (1956): 1 + Pe^2/48",
        0.05,
    )
except ImportError:  # pragma: no cover - numpy/scipy not installed
    pass


def main() -> int:
    lines = [
        "# Validation report",
        "",
        "Generated by `python docs/validate.py`. Each row compares a `fluidmech` result with a",
        "published reference value or an exact analytical solution. `Tol.` is the acceptance tolerance",
        "(relative) - correlations are only expected to match within their stated accuracy.",
        "",
    ]
    failures = 0
    group = None
    for grp, quantity, ref, comp, source, tol in CASES:
        if grp != group:
            lines += [
                "",
                f"## {grp}",
                "",
                "| Quantity | Reference | fluidmech | Error | Tol. | Source | |",
                "|---|---:|---:|---:|---:|---|:-:|",
            ]
            group = grp
        err = abs(comp - ref) / abs(ref)
        ok = err <= tol
        failures += not ok
        lines.append(
            f"| {quantity} | {ref:.5g} | {comp:.5g} | {err:.2%} | {tol:.1%} | {source} | {'✅' if ok else '❌'} |"
        )
    lines += ["", f"**{len(CASES) - failures} of {len(CASES)} checks pass.**", ""]
    Path(__file__).with_name("VALIDATION.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(CASES) - failures}/{len(CASES)} checks pass")
    for grp, quantity, ref, comp, _src, tol in CASES:
        if abs(comp - ref) / abs(ref) > tol:
            print(f"  FAIL {grp}: {quantity}: ref {ref}, got {comp}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
