"""
CLI Application.
"""

from .parser import build_parser
from .commands import run_command


def main():
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args()

    if args.text:
        print(run_command(args.text))


if __name__ == "__main__":
    main()