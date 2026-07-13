"""
Application settings.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """Application configuration."""

    app_name: str = "Tafazzal AI Voice Studio"
    app_version: str = "0.1.0.dev0"

    project_root: Path = Path.cwd()

    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    environment: str = os.getenv("APP_ENV", "development")

    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

    output_directory: Path = Path.cwd() / "output"

    def ensure_output_directory(self) -> None:
        self.output_directory.mkdir(parents=True, exist_ok=True)