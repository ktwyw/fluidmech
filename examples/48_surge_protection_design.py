"""Example 48 - Selecting valve closure time and pipe class against water hammer.

A 2.5 km transmission main runs at 1.8 m/s with 60 m working head. For each
pipe material, find the minimum valve closure time that keeps the peak
pressure (working + surge) within the pipe's pressure rating.
"""

from fluidmech import transients as t
from fluidmech.constants import G

rho = 1000.0  # water density [kg/m3]
L, D, V = 2500.0, 0.40, 1.8  # main length [m], diameter [m], velocity [m/s]
working_head = 60.0  # steady working pressure head [m]
p_working = rho * G * working_head

pipes = {  # material: (Young's modulus, wall thickness [m], pressure rating [bar])
    "steel": (t.PIPE_YOUNGS_MODULUS["steel"], 0.008, 25.0),
    "ductile_iron": (t.PIPE_YOUNGS_MODULUS["ductile_iron"], 0.0081, 25.0),
    "pvc": (t.PIPE_YOUNGS_MODULUS["pvc"], 0.0192, 16.0),
    "hdpe": (t.PIPE_YOUNGS_MODULUS["hdpe"], 0.0242, 10.0),
}

print(f"Main: L = {L / 1000} km, D = {D * 1000:.0f} mm, V = {V} m/s, working pressure {p_working / 1e5:.1f} bar\n")
print(f"{'material':<13} {'c [m/s]':>8} {'2L/c [s]':>9} {'Joukowsky':>10} {'rating':>7} {'min closure':>12}")
for name, (e_mod, wall, rating_bar) in pipes.items():
    c = t.wave_speed(rho, diameter=D, wall_thickness=wall, youngs_modulus=e_mod)
    dp_max = t.joukowsky_surge(rho, c, V)
    allowable = rating_bar * 1e5 - p_working  # surge the pipe can still take [Pa]
    if dp_max <= allowable:
        needed = "any"
    else:
        # Michaud: dp = 2 rho L V / tc  ->  tc = 2 rho L V / dp_allowable
        tc = 2 * rho * L * V / allowable  # Michaud: dp = 2 rho L V / tc solved for tc
        needed = f"{max(tc, t.critical_closure_time(L, c)):.0f} s"
    print(
        f"{name:<13} {c:>8.0f} {t.critical_closure_time(L, c):>9.1f} {dp_max / 1e5:>8.1f} b "
        f"{rating_bar:>5.0f} b {needed:>12}"
    )

print("\nCaution: Michaud's formula assumes a linear reduction in VELOCITY; real valves cut most")
print("of the flow in the last 10-20 % of their stroke. Specify a two-stage closure, or use")
print("surge vessels / air valves, and confirm with a full transient (method of characteristics) model.")
