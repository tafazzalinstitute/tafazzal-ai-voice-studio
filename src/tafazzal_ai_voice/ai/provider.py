"""
Unified AI Provider Manager for Tafazzal AI Voice Studio.
"""

from __future__ import annotations

from typing import Literal

from tafazzal_ai_voice.ai.google_ai import get_google_client
from tafazzal_ai_voice.ai.openai_ai import get_openai_client
from tafazzal_ai_voice.config.settings import settings
from tafazzal_ai_voice.logging.logger import get_logger


logger = get_logger(__name__)

Provider = Literal["openai", "google"]


class AIProvider:
    """
    Unified AI Provider.
    """

    def __init__(
        self,
        provider: Provider | None = None,
    ) -> None:

        self.provider = provider or self._detect_provider()

    def _detect_provider(self) -> Provider:
        """
        Automatically detect available provider.
        """

        if settings.is_openai_enabled:
            logger.info("Using OpenAI provider.")
            return "openai"

        if settings.is_google_enabled:
            logger.info("Using Google AI provider.")
            return "google"

        raise RuntimeError(
            "No AI provider configured."
        )

    def generate_text(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        """
        Generate text using selected provider.
        """

        if self.provider == "openai":

            client = get_openai_client()

            return client.generate_text(
                prompt=prompt,
                **kwargs,
            )

        if self.provider == "google":

            client = get_google_client()

            return client.generate_text(
                prompt=prompt,
            )

        raise RuntimeError(
            f"Unsupported provider: {self.provider}"
        )


_provider: AIProvider | None = None


def get_provider() -> AIProvider:
    """
    Return singleton provider.
    """

    global _provider

    if _provider is None:
        _provider = AIProvider()

    return _provider