# Week 9 - Viscous flow and pipe systems I: turbulence and head losses

**Syllabus:** Boundary layers and turbulence. Velocity profiles in turbulent flow. Head losses in pipes and accessories (Moody diagram). Pressure losses in non-circular pipes.

**Course learning outcomes:** CLO 2, 3, 4, 5  |  **Assessment:** Lab Assignment #2

**Reading:** White, Sections 6.1-6.9 and 7.1-7.4.

## Learning objectives

- Predict transition and entrance lengths.
- Use the law of the wall; decide whether a pipe is hydraulically smooth; size near-wall CFD cells (y+).
- Solve the Colebrook equation and interpret the Moody chart regions.
- Evaluate minor losses and losses in non-circular ducts (hydraulic and effective diameter).

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w09_01_transition_and_entrance_length.py`](w09_01_transition_and_entrance_length.py) | Laminar-turbulent transition and entrance length | fluidmech only |
| [`w09_02_turbulent_velocity_profile.py`](w09_02_turbulent_velocity_profile.py) | Turbulent velocity profiles and the law of the wall | matplotlib |
| [`w09_03_yplus_for_cfd_mesh.py`](w09_03_yplus_for_cfd_mesh.py) | How fine must a CFD mesh be near the wall? | fluidmech only |
| [`w09_04_colebrook_and_moody_regions.py`](w09_04_colebrook_and_moody_regions.py) | Solving the Colebrook equation and reading the Moody chart | fluidmech only |
| [`w09_05_minor_losses.py`](w09_05_minor_losses.py) | Minor losses in fittings, valves and area changes | fluidmech only |
| [`w09_06_noncircular_ducts.py`](w09_06_noncircular_ducts.py) | Pressure loss in non-circular ducts | fluidmech only |
| [`w09_07_flat_plate_boundary_layer.py`](w09_07_flat_plate_boundary_layer.py) | Boundary layer on a flat plate | fluidmech only |
| [`w09_08_control_valve_sizing.py`](w09_08_control_valve_sizing.py) | Valve flow coefficients (Kv, Cv) and control-valve sizing | fluidmech only |
| [`w09_09_regime_from_pressure_data.py`](w09_09_regime_from_pressure_data.py) | Identifying the flow regime from pressure-drop measurements | fluidmech only |
| [`w09_10_gas_pipeline.py`](w09_10_gas_pipeline.py) | Pressure drop in a long gas pipeline (isothermal compressible flow) | fluidmech only |
| [`w09_11_roughness_from_test_data.py`](w09_11_roughness_from_test_data.py) | Finding the roughness of an old pipe from a flow test | fluidmech only |
| [`w09_12_explicit_design_formulas.py`](w09_12_explicit_design_formulas.py) | Explicit Swamee-Jain formulas for Type 2 and Type 3 problems | fluidmech only |
| [`w09_13_point_of_mean_velocity.py`](w09_13_point_of_mean_velocity.py) | Where in the pipe does the local velocity equal the mean? | fluidmech only |
| [`w09_14_ventilation_duct_and_fan.py`](w09_14_ventilation_duct_and_fan.py) | Pressure-loss budget of a ventilation duct and the fan duty point | fluidmech only |
| [`w09_15_reynolds_decomposition.py`](w09_15_reynolds_decomposition.py) | What is 'turbulent velocity'? Reynolds decomposition of a signal | fluidmech only |
| [`w09_lab2_rectangular_duct_fd.py`](w09_lab2_rectangular_duct_fd.py) | Laminar flow in a rectangular duct by finite differences | numpy, matplotlib |

Run a script from this folder, e.g. `python w09_01_transition_and_entrance_length.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Run Lab 2 (`w09_lab2`) at n = 21, 41, 81 and plot the fRe error against grid spacing.
2. Estimate the first-cell height for your COMSOL lab geometry with `w09_03`.
3. How much does 25 years of ageing change the pumping power for the main in `w09_04`?
