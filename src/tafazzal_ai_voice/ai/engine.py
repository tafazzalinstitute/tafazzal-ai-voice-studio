"""
Base AI engine.
"""

from abc import ABC, abstractmethod


class AIEngine(ABC):
    """Base interface for AI providers."""

    @abstractmethod
    def generate(self, prompt: str):
        """Generate response."""
        raise NotImplementedError