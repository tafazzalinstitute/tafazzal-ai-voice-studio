"""
CLI Parser.
"""

import argparse


def build_parser():
    """Build CLI parser."""

    parser = argparse.ArgumentParser(
        prog="tafazzal-ai-voice",
        description="Tafazzal AI Voice Studio CLI",
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Text to convert into voice.",
    )

    return parser