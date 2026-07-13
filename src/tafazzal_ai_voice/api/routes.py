"""
API Routes.
"""

from .responses import success


def generate_voice(text: str):
    """Generate voice."""

    return success(f"Voice generated for: {text}")