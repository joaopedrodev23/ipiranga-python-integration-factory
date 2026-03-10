"""
CLI entry point for the Ipiranga Python Integration Factory generator.

Usage:
    python -m generator.cli --spec examples/rest_service.yml --output ./generated
"""

import argparse
import sys
from pathlib import Path

from generator.spec_loader import load_spec
from generator.validators import SpecValidationError, validate_spec
from generator.scaffold import create_output_dir
from generator.renderers.rest_renderer import RestRenderer

_SUPPORTED_TYPES: frozenset[str] = frozenset({"rest"})


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="generator",
        description="Ipiranga Integration Factory - microservice generator",
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

    # Step 1 - Load the YAML spec
    print(f"[1/4] Loading spec from: {spec_path}")
    try:
        spec = load_spec(str(spec_path))
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] Failed to load spec: {exc}", file=sys.stderr)
        sys.exit(1)

    # Step 2 - Validate the spec
    print("[2/4] Validating spec ...")
    try:
        validate_spec(spec)
    except SpecValidationError as exc:
        print(f"[ERROR] Spec validation failed: {exc}", file=sys.stderr)
        sys.exit(1)

    service_name: str = spec["service"]["name"]
    service_type: str = spec["service"]["type"]
    print(f"      [OK] service.name = '{service_name}'")
    print(f"      [OK] service.type = '{service_type}'")

    # Step 3 - Prepare output directory
    print(f"[3/4] Preparing output directory: {output_path}")
    try:
        create_output_dir(str(output_path))
    except OSError as exc:
        print(f"[ERROR] Could not create output directory: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"      [OK] Output directory ready: {output_path.resolve()}")

    # Step 4 - Dispatch to the correct renderer
    print(f"[4/4] Generating {service_type} service ...")
    try:
        if service_type == "rest":
            renderer = RestRenderer(spec)
            renderer.render(str(output_path))
        else:
            print(
                f"[ERROR] Unsupported service type '{service_type}'. "
                f"Supported: {sorted(_SUPPORTED_TYPES)}",
                file=sys.stderr,
            )
            sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Generation failed: {exc}", file=sys.stderr)
        sys.exit(1)

    service_dir = (output_path / service_name).resolve()
    print()
    print(f"Generated REST service: {service_name}")
    print(f"Output: {service_dir}")


if __name__ == "__main__":
    run(sys.argv[1:])
