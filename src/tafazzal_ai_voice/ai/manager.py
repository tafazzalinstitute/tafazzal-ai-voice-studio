"""
AI Manager.
"""

from .google_ai import GoogleAI
from .openai_ai import OpenAIEngine


class AIManager:
    """Manage AI providers."""

    def __init__(self):
        self.google = GoogleAI()
        self.openai = OpenAIEngine()

    def google_generate(self, prompt: str):
        return self.google.generate(prompt)

    def openai_generate(self, prompt: str):
        return self.openai.generate(prompt)