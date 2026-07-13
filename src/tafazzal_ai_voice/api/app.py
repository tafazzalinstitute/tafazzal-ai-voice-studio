"""
API Application.
"""

from .routes import generate_voice


class APIApplication:
    """Simple API application."""

    def generate(self, text: str):
        return generate_voice(text)