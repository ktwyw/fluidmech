# Week 6 - Exact solutions: plates, Couette flow, tubes and annuli

**Syllabus:** Use of Navier-Stokes equations to characterise flow profiles in simple geometries: parallel plates, Couette flow, circular tubes, tubes with annulus.

**Course learning outcomes:** CLO 2, 3, 4  |  **Assessment:** HW-4

**Reading:** White, Sections 4.10 and 6.4, 6.8. Bird, Stewart & Lightfoot, Ch. 2.

## Learning objectives

- Derive and apply velocity profiles, flow rates and wall stresses for plates, pipes, annuli and films.
- Analyse capillary viscometers with the Rabinowitsch-Mooney correction.
- Explain why laminar friction in non-circular ducts differs from the pipe value.
- Extend pipe flow to power-law and Bingham fluids.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w06_01_microchannel_and_slit.py`](w06_01_microchannel_and_slit.py) | Pressure-driven flow in a microchannel and a slit | fluidmech only |
| [`w06_02_couette_poiseuille_lubrication.py`](w06_02_couette_poiseuille_lubrication.py) | Couette-Poiseuille flow - lubrication, coating and back-flow | matplotlib |
| [`w06_03_capillary_viscometer.py`](w06_03_capillary_viscometer.py) | Capillary viscometry with the Rabinowitsch-Mooney correction | fluidmech only |
| [`w06_04_annulus_double_pipe.py`](w06_04_annulus_double_pipe.py) | Laminar flow in a concentric annulus (double-pipe heat exchanger) | matplotlib |
| [`w06_05_falling_film_column.py`](w06_05_falling_film_column.py) | Falling liquid films (wetted-wall columns, absorbers, evaporators) | fluidmech only |
| [`w06_06_non_newtonian_pipe_flow.py`](w06_06_non_newtonian_pipe_flow.py) | Pipe flow of non-Newtonian fluids | matplotlib |
| [`w06_07_taylor_couette_viscometer.py`](w06_07_taylor_couette_viscometer.py) | Flow between rotating cylinders (exact) and its stability | fluidmech only |
| [`w06_08_two_immiscible_layers.py`](w06_08_two_immiscible_layers.py) | Two immiscible liquids between parallel plates | fluidmech only |
| [`w06_09_wire_coating.py`](w06_09_wire_coating.py) | Wire coating - annular Couette flow | fluidmech only |
| [`w06_10_parallel_capillaries.py`](w06_10_parallel_capillaries.py) | Flow maldistribution among parallel laminar channels | fluidmech only |
| [`w06_11_power_law_slit_die.py`](w06_11_power_law_slit_die.py) | Polymer extrusion through a slit die (power-law fluid) | fluidmech only |
| [`w06_12_cone_and_plate_rheometer.py`](w06_12_cone_and_plate_rheometer.py) | The cone-and-plate rheometer | fluidmech only |
| [`w06_13_draining_through_a_capillary.py`](w06_13_draining_through_a_capillary.py) | Draining a tank through a long laminar tube | fluidmech only |
| [`w06_14_piston_leakage.py`](w06_14_piston_leakage.py) | Leakage past a piston or valve spool (narrow annular gap) | fluidmech only |
| [`w06_15_viscosity_from_velocity_profile.py`](w06_15_viscosity_from_velocity_profile.py) | Measuring viscosity from a velocity profile (inverse problem) | fluidmech only |

Run a script from this folder, e.g. `python w06_01_microchannel_and_slit.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Find the pressure gradient that gives zero net flow in a Couette-Poiseuille device with U = 0.5 m/s.
2. Compute the flow-rate error of the hydraulic-diameter approach for an annulus with k = 0.2.
3. Design a falling-film absorber tube bundle for a given liquid load (film Re < 1600).
