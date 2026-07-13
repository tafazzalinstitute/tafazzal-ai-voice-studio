"""
Application Entry Point.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tafazzal_ai_voice.cli.parser import (
    CLIParser,
)
from tafazzal_ai_voice.logging.logger import logger


class ApplicationError(Exception):
    """
    Raised when application startup fails.
    """


@dataclass(slots=True)
class ApplicationConfig:
    """
    Runtime configuration.
    """

    output_directory: Path
    default_voice: str


class TafazzalApplication:
    """
    Main application bootstrap.

    Desktop GUI, CLI and future API
    will all start from here.
    """

    def __init__(self) -> None:

        self.parser = CLIParser()

        self.config = ApplicationConfig(
            output_directory=Path("output"),
            default_voice="google_bn_male",
        )

        logger.info(
            "Application initialized."
        )

    def startup(self) -> None:
        """
        Initialize runtime.
        """

        self.config.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "Startup completed."
        )    def health_check(
        self,
    ) -> dict[str, object]:
        """
        Verify application components.
        """

        logger.info(
            "Running application health check."
        )

        return {
            "application": "healthy",
            "cli": self.parser.health_check(),
            "status": "healthy",
        }

    def run(
        self,
        text: str,
        output_file: str | Path,
        voice_id: str | None = None,
    ) -> Path:
        """
        Execute a complete voice generation workflow.
        """

        self.startup()

        selected_voice = (
            voice_id
            if voice_id
            else self.config.default_voice
        )

        try:

            logger.info(
                "Starting voice generation workflow."
            )

            result = self.parser.execute(
                text=text,
                output_file=output_file,
                voice_id=selected_voice,
            )

            logger.info(
                "Workflow completed successfully."
            )

            return result

        except Exception as exc:

            logger.exception(
                "Application execution failed."
            )

            raise ApplicationError(
                str(exc)
            ) from exc

    def system_info(
        self,
    ) -> dict[str, object]:
        """
        Return runtime information.
        """

        return {
            "application": "Tafazzal AI Voice Studio",
            "version": "1.1",
            "output_directory": str(
                self.config.output_directory
            ),
            "default_voice": self.config.default_voice,
            "cli": self.parser.system_info(),
            "status": "ready",
        }def main() -> int:
    """
    Application entry point.

    Returns:
        Exit status code.
    """

    app = TafazzalApplication()

    try:

        app.startup()

        logger.info(
            "Tafazzal AI Voice Studio started successfully."
        )

        return 0

    except Exception as exc:

        logger.exception(
            "Application startup failed."
        )

        raise ApplicationError(
            str(exc)
        ) from exc


application = TafazzalApplication()


if __name__ == "__main__":

    raise SystemExit(main())