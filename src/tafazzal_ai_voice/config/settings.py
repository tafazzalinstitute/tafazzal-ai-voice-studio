"""
Production configuration for Tafazzal AI Voice Studio.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(slots=True)
class Settings:
    """Application settings."""

    app_name: str = "Tafazzal AI Voice Studio"
    app_version: str = "1.1.0-dev"

    environment: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")

    openai_model: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.5",
    )

    google_model: str = os.getenv(
        "GOOGLE_MODEL",
        "gemini-2.5-flash",
    )

    output_directory: Path = PROJECT_ROOT / "output"

    log_directory: Path = PROJECT_ROOT / "logs"

    temp_directory: Path = PROJECT_ROOT / "temp"

    def create_directories(self) -> None:
        """Create required project directories."""

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.temp_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    @property
    def is_openai_enabled(self) -> bool:
        """Return True if OpenAI is configured."""

        return bool(self.openai_api_key)

    @property
    def is_google_enabled(self) -> bool:
        """Return True if Google AI is configured."""

        return bool(self.google_api_key)


settings = Settings()

settings.create_directories()