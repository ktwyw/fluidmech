"""Command-line interface: quick engineering calculations from the terminal.

Run ``fluidmech --help`` (or ``python -m fluidmech --help``) for usage.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import __version__
from . import pipe_flow as pf
from .open_channel import MANNING_N, TrapezoidalChannel
from .properties import Fluid, water_vapor_pressure
from .units import available_units, convert


def _fluid(args: argparse.Namespace) -> Fluid:
    return Fluid.air(args.temperature) if args.fluid == "air" else Fluid.water(args.temperature)


def _roughness(value: str) -> float:
    if value in pf.ROUGHNESS:
        return pf.ROUGHNESS[value]
    try:
        return float(value) / 1000.0  # given in mm
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"roughness must be a number in mm or one of: {', '.join(pf.ROUGHNESS)}"
        ) from None


def _cmd_props(args: argparse.Namespace) -> None:
    f = _fluid(args)
    print(f"{f.name}")
    print(f"  density              {f.density:.4f} kg/m3")
    print(f"  dynamic viscosity    {f.dynamic_viscosity:.4e} Pa s")
    print(f"  kinematic viscosity  {f.kinematic_viscosity:.4e} m2/s")
    if args.fluid == "water":
        print(f"  vapour pressure      {water_vapor_pressure(args.temperature) / 1e3:.3f} kPa")


def _cmd_pipe(args: argparse.Namespace) -> None:
    fluid = _fluid(args)
    eps = args.roughness
    given = sum(x is not None for x in (args.flow, args.diameter, args.head_loss))
    if given != 2:
        raise SystemExit("pipe: give exactly two of --flow, --diameter, --head-loss.")
    if args.head_loss is None:
        q, d = args.flow, args.diameter
    elif args.flow is None:
        d = args.diameter
        q = pf.flow_rate_for_head_loss(args.head_loss, d, args.length, fluid, eps, args.k_minor)
        print(f"Flow rate for {args.head_loss} m head loss: Q = {q:.5f} m3/s ({q * 1000:.2f} L/s)")
    else:
        q = args.flow
        d = pf.diameter_for_head_loss(q, args.head_loss, args.length, fluid, eps, args.k_minor)
        print(f"Diameter for {args.head_loss} m head loss: D = {d:.4f} m ({d * 1000:.1f} mm)")
    r = pf.head_loss(q, d, args.length, fluid, eps, args.k_minor)
    print(f"Pipe D = {d * 1000:.1f} mm, L = {args.length} m, eps = {eps * 1000:.4f} mm, sum K = {args.k_minor}")
    print(f"  fluid            {fluid.name}")
    print(f"  flow rate        {q * 1000:.3f} L/s")
    print(f"  velocity         {r.velocity:.3f} m/s")
    print(f"  Reynolds number  {r.reynolds:.4g} ({r.regime})")
    print(f"  friction factor  {r.friction_factor:.5f}")
    print(f"  major head loss  {r.major_head_loss:.3f} m")
    print(f"  minor head loss  {r.minor_head_loss:.3f} m")
    print(f"  total head loss  {r.total_head_loss:.3f} m  ({r.pressure_drop / 1e3:.2f} kPa)")


def _cmd_channel(args: argparse.Namespace) -> None:
    ch = TrapezoidalChannel(args.width, args.side_slope)
    n = MANNING_N.get(args.manning, None) if isinstance(args.manning, str) else args.manning
    if n is None:
        try:
            n = float(args.manning)
        except ValueError:
            raise SystemExit(f"manning must be a number or one of: {', '.join(MANNING_N)}") from None
    yn = ch.normal_depth(args.flow, n, args.slope)
    yc = ch.critical_depth(args.flow)
    print(f"Channel b = {args.width} m, z = {args.side_slope}, n = {n}, S0 = {args.slope}, Q = {args.flow} m3/s")
    print(f"  normal depth     {yn:.4f} m")
    print(f"  critical depth   {yc:.4f} m")
    print(f"  velocity         {args.flow / ch.area(yn):.3f} m/s")
    print(f"  Froude number    {ch.froude(yn, args.flow):.3f} ({ch.flow_type(yn, args.flow)})")
    print(f"  slope type       {'mild' if yn > yc else 'steep'}")


def _cmd_convert(args: argparse.Namespace) -> None:
    if args.list:
        print(" ".join(available_units()))
        return
    if args.value is None or args.from_unit is None or args.to_unit is None:
        raise SystemExit("convert: usage: fluidmech convert VALUE FROM TO   (or --list)")
    print(f"{args.value:g} {args.from_unit} = {convert(args.value, args.from_unit, args.to_unit):.6g} {args.to_unit}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fluidmech", description="Engineering fluid mechanics calculator (SI units).")
    parser.add_argument("--version", action="version", version=f"fluidmech {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_fluid(p: argparse.ArgumentParser) -> None:
        p.add_argument("--fluid", choices=["water", "air"], default="water")
        p.add_argument("-T", "--temperature", type=float, default=20.0, help="temperature [degC] (default 20)")

    p = sub.add_parser("props", help="fluid properties")
    add_fluid(p)
    p.set_defaults(func=_cmd_props)

    p = sub.add_parser(
        "pipe",
        help="pipe head loss / flow rate / diameter (give two of Q, D, h_L)",
        description="Solves the three classic pipe problems. Give exactly two of --flow, --diameter and --head-loss.",
    )
    p.add_argument("-Q", "--flow", type=float, help="flow rate [m3/s]")
    p.add_argument("-D", "--diameter", type=float, help="inside diameter [m]")
    p.add_argument("--head-loss", type=float, help="total head loss [m]")
    p.add_argument("-L", "--length", type=float, required=True, help="pipe length [m]")
    p.add_argument(
        "-e",
        "--roughness",
        type=_roughness,
        default=0.0,
        help="roughness in mm, or a material name e.g. commercial_steel",
    )
    p.add_argument("-K", "--k-minor", type=float, default=0.0, help="sum of minor-loss coefficients")
    add_fluid(p)
    p.set_defaults(func=_cmd_pipe)

    p = sub.add_parser("channel", help="normal and critical depth in a trapezoidal channel")
    p.add_argument("-Q", "--flow", type=float, required=True, help="discharge [m3/s]")
    p.add_argument("-b", "--width", type=float, required=True, help="bottom width [m]")
    p.add_argument("-z", "--side-slope", type=float, default=0.0, help="side slope z (H:V), 0 = rectangular")
    p.add_argument("-n", "--manning", default="finished_concrete", help="Manning n or a material name")
    p.add_argument("-S", "--slope", type=float, required=True, help="bed slope [m/m]")
    p.set_defaults(func=_cmd_channel)

    p = sub.add_parser("convert", help="unit conversion, e.g. 'convert 100 gpm L/s'")
    p.add_argument("value", type=float, nargs="?")
    p.add_argument("from_unit", nargs="?")
    p.add_argument("to_unit", nargs="?")
    p.add_argument("--list", action="store_true", help="list known units")
    p.set_defaults(func=_cmd_convert)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
