"""
Production CLI Commands.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tafazzal_ai_voice.logging.logger import logger
from tafazzal_ai_voice.voice.engine import VoiceEngine


class CLICommandError(Exception):
    """
    Raised when CLI command execution fails.
    """


@dataclass(slots=True)
class GenerateVoiceCommand:
    """
    Voice generation command.
    """

    text: str
    output_file: Path
    voice_id: str


class CLICommandService:
    """
    Production CLI command service.
    """

    def __init__(self) -> None:

        self.engine = VoiceEngine()

        logger.info(
            "CLICommandService initialized."
        )

    @staticmethod
    def create_command(
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> GenerateVoiceCommand:
        """
        Create CLI command.
        """

        return GenerateVoiceCommand(
            text=text.strip(),
            output_file=Path(output_file),
            voice_id=voice_id,
        )    def generate_voice(
        self,
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> Path:
        """
        Execute voice generation command.
        """

        command = self.create_command(
            text=text,
            output_file=output_file,
            voice_id=voice_id,
        )

        try:

            logger.info(
                "Executing generate voice command."
            )

            result = self.engine.generate(
                text=command.text,
                output_file=command.output_file,
                voice_id=command.voice_id,
            )

            logger.info(
                "Voice generation command completed."
            )

            return result

        except Exception as exc:

            logger.exception(
                "Generate voice command failed."
            )

            raise CLICommandError(
                str(exc)
            ) from exc

    def process_audio(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:
        """
        Execute audio processing command.
        """

        logger.info(
            "Executing audio processing command."
        )

        return self.engine.process_audio(
            input_file=input_file,
            output_file=output_file,
        )

    def available_voices(
        self,
    ) -> list[str]:
        """
        Return available voice IDs.
        """

        return self.engine.available_voices()
            def cli_info(
        self,
    ) -> dict[str, object]:
        """
        Return CLI information.
        """

        return {
            "service": "CLICommandService",
            "version": "1.1",
            "status": "ready",
        }

    def health_check(
        self,
    ) -> dict[str, object]:
        """
        Return CLI health report.
        """

        return {
            "cli": "healthy",
            "engine": self.engine.health_check(),
            "status": "healthy",
        }

    def system_info(
        self,
    ) -> dict[str, object]:
        """
        Return complete CLI runtime information.
        """

        return {
            "cli": self.cli_info(),
            "engine": self.engine.system_info(),
            "voices": self.available_voices(),
            "status": "ready",
        }


cli_command_service = CLICommandService()