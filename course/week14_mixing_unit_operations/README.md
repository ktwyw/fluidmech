# Week 14 - Fluid mechanics in ChemE unit operations: mixing

**Syllabus:** Importance of fluid dynamics in unit operations such as mixing; macro- and micro-level mixing and its role in chemical reactions.

**Course learning outcomes:** CLO 2, 3, 4, 5

**Reading:** McCabe, Smith & Harriott: agitation and mixing of liquids.

## Learning objectives

- Use power curves to compute impeller power in laminar and turbulent regimes.
- Estimate blend time, turbulence scales and micromixing time; compare with reaction time (Damkohler number).
- Evaluate scale-up rules and their consequences.
- Relate residence-time distribution and micromixing to conversion and selectivity.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w14_01_impeller_power_curves.py`](w14_01_impeller_power_curves.py) | Power curves of stirred-tank impellers | matplotlib |
| [`w14_02_stirred_tank_design.py`](w14_02_stirred_tank_design.py) | Analysing a stirred reactor | fluidmech only |
| [`w14_03_scale_up.py`](w14_03_scale_up.py) | Scaling up a stirred tank - you cannot keep everything constant | fluidmech only |
| [`w14_04_micromixing_and_reaction.py`](w14_04_micromixing_and_reaction.py) | Macro-, meso- and micromixing versus reaction speed | fluidmech only |
| [`w14_05_rtd_and_reactor_conversion.py`](w14_05_rtd_and_reactor_conversion.py) | Residence-time distribution (RTD) and conversion | matplotlib |
| [`w14_06_mixing_sensitive_reactions.py`](w14_06_mixing_sensitive_reactions.py) | How micromixing changes product selectivity | fluidmech only |
| [`w14_07_solids_suspension_zwietering.py`](w14_07_solids_suspension_zwietering.py) | Suspending solids - the just-suspended speed (Zwietering 1958) | fluidmech only |
| [`w14_08_gas_liquid_oxygen_transfer.py`](w14_08_gas_liquid_oxygen_transfer.py) | Oxygen transfer in an aerated stirred fermenter | fluidmech only |
| [`w14_09_static_mixer_laminar_mixing.py`](w14_09_static_mixer_laminar_mixing.py) | Laminar mixing - stretching and folding in a static mixer | fluidmech only |
| [`w14_10_agitator_heat_load.py`](w14_10_agitator_heat_load.py) | Agitator power becomes heat - viscous batches warm up | fluidmech only |
| [`w14_11_pumping_capacity_circulation.py`](w14_11_pumping_capacity_circulation.py) | Impeller pumping capacity and circulation time | fluidmech only |
| [`w14_12_shear_sensitive_mixing.py`](w14_12_shear_sensitive_mixing.py) | Agitating shear-sensitive material (cells, crystals, flocs) | fluidmech only |
| [`w14_13_is_the_cstr_ideal.py`](w14_13_is_the_cstr_ideal.py) | Is a continuous stirred tank really 'perfectly mixed'? | fluidmech only |
| [`w14_14_tanks_in_series_from_tracer.py`](w14_14_tanks_in_series_from_tracer.py) | Characterising a real vessel from a tracer test | fluidmech only |
| [`w14_15_segregation_and_reaction_order.py`](w14_15_segregation_and_reaction_order.py) | Does micromixing change conversion? It depends on reaction order | fluidmech only |

Run a script from this folder, e.g. `python w14_01_impeller_power_curves.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Scale up `w14_06`: which E (and hence P/V) keeps the by-product below 5 %?
2. Compare a laminar tube and 3 CSTRs in series for a second-order reaction (extend `w14_05`).
3. Find the pilot speed that gives the same micromixing time as the full-scale tank in `w14_03`.
