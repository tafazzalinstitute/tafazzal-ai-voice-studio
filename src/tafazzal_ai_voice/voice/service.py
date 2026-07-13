"""
Production Voice Service.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tafazzal_ai_voice.voice.manager import (
    VoiceManager,
)
from tafazzal_ai_voice.voice.voices import (
    VoiceProfile,
    VoiceRegistry,
)
from tafazzal_ai_voice.logging.logger import logger


class VoiceServiceError(Exception):
    """
    Raised when voice service fails.
    """


@dataclass(slots=True)
class VoiceServiceRequest:
    """
    Voice service request.
    """

    text: str
    output_file: Path
    voice_id: str


class VoiceService:
    """
    Production Voice Service.

    This class is the single business entry point
    for future Desktop GUI, CLI and API.
    """

    def __init__(self) -> None:

        self.manager = VoiceManager()

        self.registry = VoiceRegistry()

        logger.info(
            "VoiceService initialized."
        )

    def create_request(
        self,
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> VoiceServiceRequest:
        """
        Create validated request.
        """

        profile = self.registry.get(
            voice_id,
        )

        return VoiceServiceRequest(
            text=text.strip(),
            output_file=Path(output_file),
            voice_id=profile.name,
        )

    def voice_profile(
        self,
        voice_id: str,
    ) -> VoiceProfile:
        """
        Return voice profile.
        """

        return self.registry.get(
            voice_id,
        )    def generate(
        self,
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> Path:
        """
        Generate voice using the selected profile.
        """

        request = self.create_request(
            text=text,
            output_file=output_file,
            voice_id=voice_id,
        )

        try:

            profile = self.voice_profile(
                voice_id,
            )

            logger.info(
                "Generating voice using %s (%s).",
                profile.provider.value,
                profile.name,
            )

            result = self.manager.generate_to_file(
                text=request.text,
                output_file=request.output_file,
                provider=profile.provider.value,
            )

            logger.info(
                "Voice generation completed."
            )

            return result

        except Exception as exc:

            logger.exception(
                "Voice generation failed."
            )

            raise VoiceServiceError(
                str(exc)
            ) from exc

    def process_audio(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:
        """
        Process audio using the production pipeline.
        """

        logger.info(
            "Processing audio through VoiceService."
        )

        return self.manager.process_audio(
            input_file=input_file,
            output_file=output_file,
        )

    def available_voices(
        self,
    ) -> list[str]:
        """
        Return all available voice IDs.
        """

        return self.registry.voice_ids()
            def default_voice(
        self,
    ) -> VoiceProfile:
        """
        Return the default voice profile.
        """

        return self.registry.default_voice()

    def health_check(
        self,
    ) -> dict[str, object]:
        """
        Voice service health report.
        """

        return {
            "voice_manager": "healthy",
            "voice_registry": "healthy",
            "audio_pipeline": self.manager.pipeline.health_check(),
            "default_voice": self.default_voice().name,
            "status": "healthy",
        }

    def system_info(
        self,
    ) -> dict[str, object]:
        """
        Return service information.
        """

        return {
            "service": "VoiceService",
            "version": "1.1",
            "default_voice": self.default_voice().name,
            "voices": len(self.available_voices()),
            "manager": self.manager.system_info(),
            "status": "ready",
        }


voice_service = VoiceService()