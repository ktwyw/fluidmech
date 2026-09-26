# Week 13 - Dimensional analysis and similarity

**Syllabus:** Buckingham Pi theorem. Main dimensionless groups in fluid mechanics. Application of dimensional analysis.

**Course learning outcomes:** CLO 1, 2, 3, 4, 5  |  **Assessment:** HW-7

**Reading:** White, Ch. 5.

## Learning objectives

- Form Pi groups by hand and verify them with the automatic solver.
- Collapse experimental data with dimensionless groups.
- Scale model tests (pumps, meters, tanks) and recognise when full similarity is impossible.
- Interpret the main dimensionless groups of chemical engineering.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w13_01_buckingham_pi_pipe_flow.py`](w13_01_buckingham_pi_pipe_flow.py) | Buckingham Pi for pipe flow, and why it works | fluidmech only |
| [`w13_02_pi_groups_catalogue.py`](w13_02_pi_groups_catalogue.py) | Pi groups for classic problems, found automatically | fluidmech only |
| [`w13_03_pump_similarity.py`](w13_03_pump_similarity.py) | Pump similarity and the affinity laws | fluidmech only |
| [`w13_04_model_testing.py`](w13_04_model_testing.py) | Model testing and the limits of similarity | fluidmech only |
| [`w13_05_dimensionless_groups_in_chme.py`](w13_05_dimensionless_groups_in_chme.py) | The dimensionless groups a chemical engineer meets | fluidmech only |
| [`w13_06_repeating_variables_by_hand.py`](w13_06_repeating_variables_by_hand.py) | The method of repeating variables, step by step | sympy |
| [`w13_07_data_collapse_sphere_drag.py`](w13_07_data_collapse_sphere_drag.py) | Collapsing drag data with dimensionless groups | fluidmech only |
| [`w13_08_nondimensional_navier_stokes.py`](w13_08_nondimensional_navier_stokes.py) | Non-dimensionalising the Navier-Stokes equations | sympy |
| [`w13_09_maximum_drop_size_hinze.py`](w13_09_maximum_drop_size_hinze.py) | Dimensional reasoning for drop break-up (Kolmogorov-Hinze) | fluidmech only |
| [`w13_10_fitting_a_correlation.py`](w13_10_fitting_a_correlation.py) | Finding a dimensionless correlation from experiments | fluidmech only |
| [`w13_11_weir_from_one_experiment.py`](w13_11_weir_from_one_experiment.py) | Dimensional analysis plus ONE experiment gives a design formula | fluidmech only |
| [`w13_12_reynolds_independence.py`](w13_12_reynolds_independence.py) | Reynolds-number independence in wind-tunnel testing | fluidmech only |
| [`w13_13_sloshing_frequency.py`](w13_13_sloshing_frequency.py) | Sloshing of liquid in a tank - scaling and the natural frequency | fluidmech only |
| [`w13_14_bubble_size_at_orifice.py`](w13_14_bubble_size_at_orifice.py) | Bubble size from a sparger orifice - a force balance in Pi groups | fluidmech only |
| [`w13_15_drain_time_scaling.py`](w13_15_drain_time_scaling.py) | Scaling the draining time of a tank | fluidmech only |

Run a script from this folder, e.g. `python w13_01_buckingham_pi_pipe_flow.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Use `fluidmech.dimensional.pi_groups` to check every dimensional-analysis question in HW-7.
2. Choose different repeating variables for the pump problem and show that the new groups are products of the old ones.
3. Design a 1:5 model test of a spray nozzle: which group can you match, and which cannot?
