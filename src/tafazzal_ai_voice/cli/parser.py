"""
Production CLI Argument Parser.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tafazzal_ai_voice.cli.commands import (
    CLICommandService,
)
from tafazzal_ai_voice.logging.logger import logger


class CLIParserError(Exception):
    """
    Raised when CLI parsing fails.
    """


@dataclass(slots=True)
class CLIArguments:
    """
    Parsed CLI arguments.
    """

    text: str
    output_file: Path
    voice_id: str


class CLIParser:
    """
    Production CLI Parser.
    """

    def __init__(self) -> None:

        self.commands = CLICommandService()

        logger.info(
            "CLIParser initialized."
        )

    @staticmethod
    def parse(
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> CLIArguments:
        """
        Parse CLI arguments.
        """

        return CLIArguments(
            text=text.strip(),
            output_file=Path(output_file),
            voice_id=voice_id.strip(),
        )    def validate(
        self,
        arguments: CLIArguments,
    ) -> CLIArguments:
        """
        Validate parsed CLI arguments.
        """

        if not arguments.text:
            raise CLIParserError(
                "Text cannot be empty."
            )

        if not arguments.voice_id:
            raise CLIParserError(
                "Voice ID cannot be empty."
            )

        arguments.output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        voices = self.commands.available_voices()

        if arguments.voice_id not in voices:
            raise CLIParserError(
                f"Unknown voice: {arguments.voice_id}"
            )

        return arguments

    def execute(
        self,
        text: str,
        output_file: str | Path,
        voice_id: str,
    ) -> Path:
        """
        Execute CLI command.
        """

        arguments = self.validate(
            self.parse(
                text=text,
                output_file=output_file,
                voice_id=voice_id,
            )
        )

        try:

            logger.info(
                "Executing CLI parser."
            )

            result = self.commands.generate_voice(
                text=arguments.text,
                output_file=arguments.output_file,
                voice_id=arguments.voice_id,
            )

            logger.info(
                "CLI execution completed."
            )

            return result

        except Exception as exc:

            logger.exception(
                "CLI execution failed."
            )

            raise CLIParserError(
                str(exc)
            ) from exc

    def available_voices(
        self,
    ) -> list[str]:
        """
        Return available voices.
        """

        return self.commands.available_voices()
            def parser_info(
        self,
    ) -> dict[str, object]:
        """
        Return parser information.
        """

        return {
            "parser": "CLIParser",
            "version": "1.1",
            "status": "ready",
        }

    def health_check(
        self,
    ) -> dict[str, object]:
        """
        Return parser health report.
        """

        return {
            "parser": "healthy",
            "commands": self.commands.health_check(),
            "status": "healthy",
        }

    def system_info(
        self,
    ) -> dict[str, object]:
        """
        Return complete CLI runtime information.
        """

        return {
            "parser": self.parser_info(),
            "commands": self.commands.system_info(),
            "voices": self.available_voices(),
            "status": "ready",
        }


cli_parser = CLIParser()