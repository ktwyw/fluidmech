"""CHME 202 - Week 12 - Example 5: membranes - Darcy's law at the smallest scale.

Flux J = (dp - d_pi) / (mu (R_m + R_f)). Reverse osmosis must first overcome the
osmotic pressure; ultrafiltration flux declines as a fouling layer builds up.
"""

from fluidmech import porous as por

mu = 1.0e-3  # water [Pa s]
# Reverse osmosis of seawater (~35 g/L NaCl ~ 0.6 mol/L -> 600 mol/m3, two ions)
pi_sea = por.vant_hoff_osmotic_pressure(600.0, 25.0, ions_per_formula=2)
r_ro = 6e14  # 1/m, gives the 12-20 LMH typical of seawater RO
print(f"Seawater osmotic pressure (van 't Hoff): {pi_sea / 1e5:.1f} bar\n")
print(f"{'applied dp [bar]':>17} {'flux [LMH]':>11}")
for bar in [20, 30, 40, 55, 70]:
    j = por.membrane_flux(bar * 1e5, mu, r_ro, osmotic_pressure_difference=pi_sea)  # bar -> Pa
    print(f"{bar:>17} {por.lmh(j):>11.1f}")
print("Below the osmotic pressure there is no permeate at all; seawater RO runs at ~55-70 bar.\n")

# Ultrafiltration with fouling growing linearly in time
r_m = 3e12
print("Ultrafiltration at 1.5 bar with a fouling layer that grows over a run:")
for hours in [0, 1, 2, 4, 8]:
    r_f = 1.5e12 * hours  # fouling resistance assumed to grow linearly with time [1/m]
    j = por.membrane_flux(1.5e5, mu, r_m, r_f)
    print(f"  after {hours} h: fouling R_f = {r_f:.1e} 1/m, flux {por.lmh(j):5.0f} LMH")
flow = 50.0  # m3/h plant
area = flow * 1000 / por.lmh(por.membrane_flux(1.5e5, mu, r_m, 1.5e12 * 4))
print(f"\nA {flow:.0f} m3/h plant sized on the 4-hour flux needs {area:,.0f} m2 of membrane;")
print("backwashing restores most of the flux - the reversible part of the fouling resistance.")
