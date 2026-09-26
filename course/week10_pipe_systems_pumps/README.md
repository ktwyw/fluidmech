# Week 10 - Viscous flow and pipe systems II: multiple pipes and pumps

**Syllabus:** Calculation of pressure losses in piping systems, including multiple pipe systems, and pumps.

**Course learning outcomes:** CLO 2, 3, 4, 5  |  **Assessment:** HW-5

**Reading:** White, Sections 6.9-6.11 and Ch. 11 (turbomachinery).

## Learning objectives

- Build a system curve (static, pressure and friction head) and find the pump operating point.
- Analyse series, parallel and branching pipe systems, and balance parallel branches.
- Select a pump relative to its best efficiency point and check NPSH.
- Evaluate energy use of throttling versus variable-speed control (Grundfos bridge project).

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w10_01_tank_to_reactor_transfer.py`](w10_01_tank_to_reactor_transfer.py) | Total dynamic head for a process transfer line | fluidmech only |
| [`w10_02_cooling_water_header.py`](w10_02_cooling_water_header.py) | Flow distribution in a cooling-water header (parallel branches) | fluidmech only |
| [`w10_03_pump_selection_npsh.py`](w10_03_pump_selection_npsh.py) | Selecting a pump for a duty and checking NPSH | fluidmech only |
| [`w10_04_viscous_liquids.py`](w10_04_viscous_liquids.py) | When the 'water assumption' fails - pumping viscous liquids | fluidmech only |
| [`w10_05_multiple_pipe_systems.py`](w10_05_multiple_pipe_systems.py) | Multiple-pipe systems - series, parallel and branching | fluidmech only |
| [`w10_06_closed_loop_circulator.py`](w10_06_closed_loop_circulator.py) | A closed heating loop and its circulator pump | fluidmech only |
| [`w10_07_submersible_well_pump.py`](w10_07_submersible_well_pump.py) | A submersible pump in a borehole | fluidmech only |
| [`w10_08_grundfos_bridge_project.py`](w10_08_grundfos_bridge_project.py) | Specifying the hydraulic duty for a water-supply pump | fluidmech only |
| [`w10_09_hardy_cross_by_hand.py`](w10_09_hardy_cross_by_hand.py) | A pipe loop solved by the Hardy Cross method, step by step | fluidmech only |
| [`w10_10_operating_point_drift.py`](w10_10_operating_point_drift.py) | Why the operating point moves - tank level, fouling and ageing | fluidmech only |
| [`w10_11_pump_test_rig.py`](w10_11_pump_test_rig.py) | Measuring a pump curve on a test rig | fluidmech only |
| [`w10_12_dosing_pump.py`](w10_12_dosing_pump.py) | Positive-displacement (dosing) pumps versus centrifugal pumps | fluidmech only |
| [`w10_13_filling_two_tanks.py`](w10_13_filling_two_tanks.py) | One pump filling two tanks at different levels | fluidmech only |
| [`w10_14_pump_startup_transient.py`](w10_14_pump_startup_transient.py) | How quickly does the flow build up when a pump starts? | fluidmech only |
| [`w10_15_pump_life_cycle_cost.py`](w10_15_pump_life_cycle_cost.py) | Choosing a pump on life-cycle cost, not purchase price | fluidmech only |

Run a script from this folder, e.g. `python w10_01_tank_to_reactor_transfer.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Replace the illustrative curve in `w10_08` with data exported from Grundfos Product Center for your chosen pump.
2. Repeat `w10_03` for a 90 degC liquid and redesign the suction side.
3. Add a fourth exchanger to `w10_02` and re-balance the header.
