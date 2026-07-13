"""
Production OpenAI client for Tafazzal AI Voice Studio.
"""

from __future__ import annotations

from typing import Optional

from openai import OpenAI

from tafazzal_ai_voice.config.settings import settings
from tafazzal_ai_voice.logging.logger import get_logger


logger = get_logger(__name__)


class OpenAIClient:
    """
    Production OpenAI client.
    """

    def __init__(self) -> None:

        if not settings.is_openai_enabled:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=settings.openai_api_key,
        )

        self.model = settings.openai_model

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate text from OpenAI.
        """

        messages = []

        if system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            text = response.choices[0].message.content

            logger.info("OpenAI request completed successfully.")

            return text or ""

        except Exception as exc:

            logger.exception(
                "OpenAI request failed."
            )

            raise RuntimeError(
                "OpenAI generation failed."
            ) from exc


_client: Optional[OpenAIClient] = None


def get_openai_client() -> OpenAIClient:
    """
    Return singleton OpenAI client.
    """

    global _client

    if _client is None:
        _client = OpenAIClient()

    return _client