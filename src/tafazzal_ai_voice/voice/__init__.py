"""
Voice package.
"""

from .manager import VoiceManager
from .voices import AVAILABLE_VOICES

__all__ = [
    "VoiceManager",
    "AVAILABLE_VOICES",
]