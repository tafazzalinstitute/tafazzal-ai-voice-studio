"""
Voice Manager.
"""

from .generator import VoiceGenerator
from .voices import AVAILABLE_VOICES


class VoiceManager:
    """Manage voices."""

    def __init__(self):
        self.generator = VoiceGenerator()

    def voices(self):
        return AVAILABLE_VOICES

    def generate(self, text: str):
        return self.generator.generate(text)