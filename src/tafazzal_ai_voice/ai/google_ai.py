"""
Google AI implementation.
"""

from .engine import AIEngine


class GoogleAI(AIEngine):
    """Google AI Engine."""

    def generate(self, prompt: str):
        return {
            "provider": "Google AI",
            "text": prompt,
        }