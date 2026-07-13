"""
Production Google AI client for Tafazzal AI Voice Studio.
"""

from __future__ import annotations

from typing import Optional

from google import genai

from tafazzal_ai_voice.config.settings import settings
from tafazzal_ai_voice.logging.logger import get_logger


logger = get_logger(__name__)


class GoogleAIClient:
    """
    Production Google AI client.
    """

    def __init__(self) -> None:

        if not settings.is_google_enabled:
            raise ValueError(
                "GOOGLE_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.google_api_key,
        )

        self.model = settings.google_model

    def generate_text(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text using Google AI.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            text = response.text or ""

            logger.info(
                "Google AI request completed successfully."
            )

            return text

        except Exception as exc:

            logger.exception(
                "Google AI request failed."
            )

            raise RuntimeError(
                "Google AI generation failed."
            ) from exc


_client: Optional[GoogleAIClient] = None


def get_google_client() -> GoogleAIClient:
    """
    Return singleton Google AI client.
    """

    global _client

    if _client is None:
        _client = GoogleAIClient()

    return _client