"""
CLI entry point for the Ipiranga Python Integration Factory generator.

Usage:
    python -m generator.cli --spec examples/rest_service.yml --output ./generated
"""

import argparse
import sys
from pathlib import Path

from generator.spec_loader import load_spec
from generator.validators import validate_spec
from generator.scaffold import create_output_dir


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="generator",
        description="Ipiranga Integration Factory — microservice generator",
    )
    parser.add_argument(
        "--spec",
        required=True,
        type=str,
        help="Path to the YAML specification file (e.g. examples/rest_service.yml)",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=str,
        help="Directory where the generated service will be written (e.g. ./generated)",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    spec_path = Path(args.spec)
    output_path = Path(args.output)

    # Step 1 — Load the YAML spec
    print(f"[1/4] Loading spec from: {spec_path}")
    spec = load_spec(str(spec_path))

    # Step 2 — Validate the spec
    print("[2/4] Validating spec …")
    validate_spec(spec)

    service_name: str = spec["service"]["name"]
    service_type: str = spec["service"]["type"]
    print(f"      ✔ service.name = '{service_name}'")
    print(f"      ✔ service.type = '{service_type}'")

    # Step 3 — Confirm
    print(f"[3/4] Spec is valid — service '{service_name}' (type: {service_type})")

    # Step 4 — Prepare output directory
    print(f"[4/4] Preparing output directory: {output_path}")
    create_output_dir(str(output_path))
    print(f"      ✔ Output directory ready: {output_path.resolve()}")

    print()
    print("Foundation phase complete. Generation not yet implemented.")


if __name__ == "__main__":
    run(sys.argv[1:])
