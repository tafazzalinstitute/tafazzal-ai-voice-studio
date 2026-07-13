"""
Production Voice Manager.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tafazzal_ai_voice.ai.provider import (
    AIProviderManager,
)
from tafazzal_ai_voice.audio.processor import (
    AudioPipeline,
)
from tafazzal_ai_voice.logging.logger import logger


class VoiceManagerError(Exception):
    """Raised when voice workflow fails."""


@dataclass(slots=True)
class VoiceRequest:
    """
    Voice generation request.
    """

    text: str
    output_file: Path
    provider: str = "auto"


class VoiceManager:
    """
    Unified production voice manager.
    """

    def __init__(self) -> None:

        self.provider = AIProviderManager()

        self.pipeline = AudioPipeline()

        logger.info(
            "VoiceManager initialized."
        )

    @staticmethod
    def create_request(
        text: str,
        output_file: str | Path,
        provider: str = "auto",
    ) -> VoiceRequest:
        """
        Create validated request.
        """

        return VoiceRequest(
            text=text.strip(),
            output_file=Path(output_file),
            provider=provider,
        )

    def available_provider(self) -> Any:
        """
        Return active AI provider.
        """

        return self.provider.get_provider()

    def pipeline_info(
        self,
    ) -> dict[str, object]:
        """
        Return pipeline information.
        """

        return self.pipeline.pipeline_info()
            def generate(
        self,
        text: str,
    ) -> str:
        """
        Generate voice content using the selected AI provider.
        """

        try:

            provider = self.available_provider()

            logger.info(
                "Generating content using AI provider."
            )

            response = provider.generate(
                text,
            )

            logger.info(
                "Generation completed successfully."
            )

            return response

        except Exception as exc:

            logger.exception(
                "Voice generation failed."
            )

            raise VoiceManagerError(
                str(exc)
            ) from exc

    def generate_to_file(
        self,
        text: str,
        output_file: str | Path,
        provider: str = "auto",
    ) -> Path:
        """
        Generate content and save it.
        """

        request = self.create_request(
            text=text,
            output_file=output_file,
            provider=provider,
        )

        result = self.generate(
            request.text,
        )

        request.output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        request.output_file.write_text(
            result,
            encoding="utf-8",
        )

        logger.info(
            "Generated content saved: %s",
            request.output_file,
        )

        return request.output_file

    def process_audio(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:
        """
        Process audio through the production pipeline.
        """

        logger.info(
            "Processing audio pipeline."
        )

        return self.pipeline.process(
            input_file=input_file,
            output_file=output_file,
        )    def health_check(
        self,
    ) -> dict[str, object]:
        """
        Return overall Voice Manager health.
        """

        return {
            "provider": "healthy",
            "audio_pipeline": self.pipeline.health_check(),
            "status": "healthy",
        }

    def system_info(
        self,
    ) -> dict[str, object]:
        """
        Return system information.
        """

        provider = self.available_provider()

        provider_name = (
            provider.__class__.__name__
            if provider is not None
            else "Unavailable"
        )

        return {
            "manager": "VoiceManager",
            "version": "1.1",
            "provider": provider_name,
            "pipeline": self.pipeline.pipeline_info(),
            "status": "ready",
        }


voice_manager = VoiceManager()