"""
OpenAI implementation.
"""

from .engine import AIEngine


class OpenAIEngine(AIEngine):
    """OpenAI Engine."""

    def generate(self, prompt: str):
        return {
            "provider": "OpenAI",
            "text": prompt,
        }