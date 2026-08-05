"""Command-line interface for MATRIUN."""

import argparse

from matriun import (
    add_matrices,
    create_identity_matrix,
    create_zero_matrix,
    multiply_matrices,
    scale_matrix,
    transpose_matrix,
)


def _format_matrix(matrix):
    """Return a readable multi-line matrix representation."""
    return "\n".join(f"  {row}" for row in matrix)


def _run_demo(size):
    """Print a small walkthrough of matrix operations."""
    print("MATRIUN demo")
    print(f"Matrix size: {size}x{size}")

    identity = create_identity_matrix(size)
    print("\nIdentity matrix:")
    print(_format_matrix(identity))

    zero_matrix = create_zero_matrix(size, size)
    print("\nZero matrix:")
    print(_format_matrix(zero_matrix))

    scaled_identity = scale_matrix(identity, 3)
    print("\nScaled identity (x3):")
    print(_format_matrix(scaled_identity))

    matrix_a = [[row + col for col in range(size)] for row in range(size)]
    matrix_b = transpose_matrix(matrix_a)

    print("\nMatrix A:")
    print(_format_matrix(matrix_a))
    print("\nMatrix B (transpose of A):")
    print(_format_matrix(matrix_b))

    print("\nA + B:")
    print(_format_matrix(add_matrices(matrix_a, matrix_b)))

    print("\nA * I:")
    print(_format_matrix(multiply_matrices(matrix_a, identity)))


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="matriun",
        description="MATRIUN matrix utility CLI",
    )
    subcommands = parser.add_subparsers(dest="command")

    demo_parser = subcommands.add_parser("demo", help="Run a matrix operations demo")
    demo_parser.add_argument(
        "--size",
        type=int,
        default=3,
        help="Square matrix size used in the demo (default: 3)",
    )

    return parser


def main(argv=None):
    """Run the CLI and return an exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        _run_demo(3)
        return 0

    if args.command == "demo":
        if args.size <= 0:
            parser.error("--size must be a positive integer")
        _run_demo(args.size)
        return 0

    parser.error("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main())