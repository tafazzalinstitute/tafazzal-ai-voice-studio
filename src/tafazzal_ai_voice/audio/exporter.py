"""
Production Audio Exporter

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pydub import AudioSegment

from tafazzal_ai_voice.audio.formats import (
    AudioFormatRegistry,
)
from tafazzal_ai_voice.logging.logger import logger


class AudioExportError(Exception):
    """Raised when audio export fails."""


@dataclass(slots=True)
class ExportRequest:
    """
    Audio export request.
    """

    audio: AudioSegment
    output_file: Path


class AudioExporter:
    """
    Production Audio Exporter.
    """

    def __init__(self) -> None:

        logger.info(
            "AudioExporter initialized."
        )

    @staticmethod
    def validate_output(
        output_file: str | Path,
    ) -> Path:
        """
        Validate output path.
        """

        path = Path(output_file)

        AudioFormatRegistry.from_extension(
            path.suffix
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    def create_request(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> ExportRequest:
        """
        Create export request.
        """

        request = ExportRequest(
            audio=audio,
            output_file=self.validate_output(
                output_file,
            ),
        )

        logger.info(
            "Export request created."
        )

        return request
            def export(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> Path:
        """
        Export audio to the requested format.
        """

        request = self.create_request(
            audio=audio,
            output_file=output_file,
        )

        try:

            export_format = (
                AudioFormatRegistry
                .from_extension(
                    request.output_file.suffix,
                )
                .value
            )

            logger.info(
                "Exporting audio as %s",
                export_format,
            )

            request.audio.export(
                request.output_file,
                format=export_format,
            )

            if (
                not request.output_file.exists()
                or request.output_file.stat().st_size == 0
            ):
                raise AudioExportError(
                    "Export failed."
                )

            logger.info(
                "Audio exported successfully."
            )

            return request.output_file

        except Exception as exc:

            logger.exception(
                "Audio export failed."
            )

            raise AudioExportError(
                str(exc)
            ) from exc

    def export_wav(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> Path:
        """
        Export as WAV.
        """

        return self.export(
            audio,
            output_file,
        )

    def export_mp3(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> Path:
        """
        Export as MP3.
        """

        return self.export(
            audio,
            output_file,
        )

    def export_flac(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> Path:
        """
        Export as FLAC.
        """

        return self.export(
            audio,
            output_file,
        )

    def export_ogg(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> Path:
        """
        Export as OGG.
        """

        return self.export(
            audio,
            output_file,
        )

    def export_m4a(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> Path:
        """
        Export as M4A.
        """

        return self.export(
            audio,
            output_file,
        )    @staticmethod
    def verify_output(
        output_file: str | Path,
    ) -> bool:
        """
        Verify exported audio file.
        """

        path = Path(output_file)

        return (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
        )

    @staticmethod
    def file_size(
        output_file: str | Path,
    ) -> int:
        """
        Return exported file size.
        """

        path = Path(output_file)

        if not path.exists():
            return 0

        return path.stat().st_size

    def batch_export(
        self,
        audio: AudioSegment,
        output_directory: str | Path,
        base_name: str,
        formats: list[str],
    ) -> list[Path]:
        """
        Export audio to multiple formats.
        """

        output_dir = Path(output_directory)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        exported: list[Path] = []

        for fmt in formats:

            audio_format = (
                AudioFormatRegistry.validate(fmt)
            )

            output_file = (
                output_dir
                / f"{base_name}.{audio_format.value}"
            )

            exported.append(
                self.export(
                    audio,
                    output_file,
                )
            )

        logger.info(
            "Batch export completed (%s file(s)).",
            len(exported),
        )

        return exported

    def health_check(
        self,
        output_file: str | Path,
    ) -> dict[str, object]:
        """
        Exporter health report.
        """

        path = Path(output_file)

        return {
            "exists": path.exists(),
            "verified": self.verify_output(path),
            "size": self.file_size(path),
            "extension": path.suffix.lower(),
            "status": "healthy",
        }


audio_exporter = AudioExporter()