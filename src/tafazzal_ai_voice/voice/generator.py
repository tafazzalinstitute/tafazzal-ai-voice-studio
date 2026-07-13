"""
Voice Generator.
"""


class VoiceGenerator:
    """Generate voice from text."""

    def generate(self, text: str):
        return {
            "status": "success",
            "text": text,
        }