"""
Production-ready audio processing engine.

Tafazzal AI Voice Studio
Version: 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import wave

from tafazzal_ai_voice.logging.logger import logger


SUPPORTED_AUDIO_FORMATS = {
    ".wav",
    ".mp3",
    ".flac",
    ".ogg",
    ".m4a",
}


class AudioProcessingError(Exception):
    """Raised when audio processing fails."""


@dataclass(slots=True)
class AudioMetadata:
    """
    Audio metadata.
    """

    path: Path
    duration: float
    sample_rate: int
    channels: int
    sample_width: int
    frames: int


class AudioProcessor:
    """
    Production audio processor.
    """

    def __init__(self) -> None:
        logger.info("AudioProcessor initialized.")

    @staticmethod
    def validate_file(audio_path: str | Path) -> Path:
        """
        Validate audio file.
        """

        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix.lower() not in SUPPORTED_AUDIO_FORMATS:
            raise AudioProcessingError(
                f"Unsupported audio format: {path.suffix}"
            )

        return path

    def load_metadata(
        self,
        audio_path: str | Path,
    ) -> AudioMetadata:
        """
        Load WAV metadata.
        """

        path = self.validate_file(audio_path)

        if path.suffix.lower() != ".wav":
            raise AudioProcessingError(
                "Metadata reading currently supports WAV only."
            )

        try:

            with wave.open(str(path), "rb") as audio:

                channels = audio.getnchannels()

                sample_rate = audio.getframerate()

                frames = audio.getnframes()

                sample_width = audio.getsampwidth()

                duration = frames / float(sample_rate)

            metadata = AudioMetadata(
                path=path,
                duration=duration,
                sample_rate=sample_rate,
                channels=channels,
                sample_width=sample_width,
                frames=frames,
            )

            logger.info(
                "Loaded audio metadata: %s",
                metadata.path.name,
            )

            return metadata

        except Exception as exc:

            logger.exception(
                "Failed to read audio metadata."
            )

            raise AudioProcessingError(
                str(exc)
            ) from exc

    def duration(
        self,
        audio_path: str | Path,
    ) -> float:
        """
        Return duration in seconds.
        """

        return self.load_metadata(audio_path).duration

    def sample_rate(
        self,
        audio_path: str | Path,
    ) -> int:
        """
        Return sample rate.
        """

        return self.load_metadata(audio_path).sample_rate

    def channels(
        self,
        audio_path: str | Path,
    ) -> int:
        """
        Return channel count.
        """

        return self.load_metadata(audio_path).channels
            def exists(
        self,
        audio_path: str | Path,
    ) -> bool:
        """
        Check whether the audio file exists.
        """

        try:
            self.validate_file(audio_path)
            return True
        except Exception:
            return False

    def file_size(
        self,
        audio_path: str | Path,
    ) -> int:
        """
        Return file size in bytes.
        """

        path = self.validate_file(audio_path)

        return path.stat().st_size

    def extension(
        self,
        audio_path: str | Path,
    ) -> str:
        """
        Return audio extension.
        """

        return self.validate_file(audio_path).suffix.lower()

    def summary(
        self,
        audio_path: str | Path,
    ) -> dict:
        """
        Return metadata summary.
        """

        metadata = self.load_metadata(audio_path)

        return {
            "filename": metadata.path.name,
            "path": str(metadata.path),
            "duration": metadata.duration,
            "sample_rate": metadata.sample_rate,
            "channels": metadata.channels,
            "sample_width": metadata.sample_width,
            "frames": metadata.frames,
            "size": self.file_size(audio_path),
            "extension": self.extension(audio_path),
        }

    def print_summary(
        self,
        audio_path: str | Path,
    ) -> None:
        """
        Log metadata summary.
        """

        info = self.summary(audio_path)

        logger.info("========== Audio Summary ==========")

        for key, value in info.items():
            logger.info("%s : %s", key, value)

        logger.info("===================================")
            def validate_wav(
        self,
        audio_path: str | Path,
    ) -> bool:
        """
        Validate WAV structure.
        """

        try:

            metadata = self.load_metadata(audio_path)

            return (
                metadata.channels > 0
                and metadata.sample_rate > 0
                and metadata.frames > 0
            )

        except Exception:

            return False

    def health_check(
        self,
        audio_path: str | Path,
    ) -> dict:
        """
        Production health check.
        """

        status = {
            "exists": self.exists(audio_path),
            "valid": False,
            "metadata": False,
        }

        if not status["exists"]:
            return status

        try:

            self.load_metadata(audio_path)

            status["metadata"] = True

            status["valid"] = self.validate_wav(audio_path)

        except Exception:

            logger.exception(
                "Audio health check failed."
            )

        return status


audio_processor = AudioProcessor()