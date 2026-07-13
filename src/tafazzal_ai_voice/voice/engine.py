"""
Production Voice Engine.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tafazzal_ai_voice.logging.logger import logger
from tafazzal_ai_voice.voice.service import (
    VoiceService,
)


class VoiceEngineError(Exception):
    """
    Raised when voice engine execution fails.
    """


@dataclass(slots=True)
class VoiceJob:
    """
    Voice execution job.
    """

    text: str
    output_file: Path
    voice_id: str


class VoiceEngine:
    """
    Production Voice Execution Engine.

    Entry point for:
    - Desktop GUI
    - CLI
    - API
    """

    def __init__(self) -> None:

        self.service = VoiceService()

        logger.info(
            "VoiceEngine initialized."
        )

    @staticmethod
    def create_job(
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> VoiceJob:
        """
        Create execution job.
        """

        return VoiceJob(
            text=text.strip(),
            output_file=Path(output_file),
            voice_id=voice_id,
        )

    def available_voices(
        self,
    ) -> list[str]:
        """
        Return available voices.
        """

        return self.service.available_voices()

    def default_voice(
        self,
    ):
        """
        Return default voice profile.
        """

        return self.service.default_voice()
            def execute(
        self,
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> Path:
        """
        Execute a complete voice generation job.
        """

        job = self.create_job(
            text=text,
            output_file=output_file,
            voice_id=voice_id,
        )

        try:

            logger.info(
                "Executing voice job."
            )

            result = self.service.generate(
                text=job.text,
                output_file=job.output_file,
                voice_id=job.voice_id,
            )

            logger.info(
                "Voice job completed successfully."
            )

            return result

        except Exception as exc:

            logger.exception(
                "Voice engine execution failed."
            )

            raise VoiceEngineError(
                str(exc)
            ) from exc

    def generate(
        self,
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> Path:
        """
        Generate voice output.
        """

        return self.execute(
            text=text,
            output_file=output_file,
            voice_id=voice_id,
        )

    def process_audio(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:
        """
        Process an audio file using the production pipeline.
        """

        logger.info(
            "Processing audio from VoiceEngine."
        )

        return self.service.process_audio(
            input_file=input_file,
            output_file=output_file,
        )    def engine_info(
        self,
    ) -> dict[str, object]:
        """
        Return engine information.
        """

        return {
            "engine": "VoiceEngine",
            "version": "1.1",
            "status": "ready",
        }

    def health_check(
        self,
    ) -> dict[str, object]:
        """
        Return engine health report.
        """

        return {
            "engine": "healthy",
            "service": self.service.health_check(),
            "status": "healthy",
        }

    def system_info(
        self,
    ) -> dict[str, object]:
        """
        Return complete runtime information.
        """

        return {
            "engine": self.engine_info(),
            "service": self.service.system_info(),
            "voices": self.available_voices(),
            "default_voice": self.default_voice().name,
            "status": "ready",
        }


voice_engine = VoiceEngine()