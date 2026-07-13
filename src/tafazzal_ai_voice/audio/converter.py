"""
Production Audio Converter

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from pydub import AudioSegment

from tafazzal_ai_voice.audio.formats import (
    AudioFormatRegistry,
)
from tafazzal_ai_voice.logging.logger import logger


class AudioConversionError(Exception):
    """Raised when audio conversion fails."""


@dataclass(slots=True)
class ConversionRequest:
    """
    Audio conversion request.
    """

    input_file: Path
    output_file: Path


class AudioConverter:
    """
    Production Audio Converter.
    """

    def __init__(self) -> None:

        logger.info(
            "AudioConverter initialized."
        )

    @staticmethod
    def validate_input(
        input_file: str | Path,
    ) -> Path:
        """
        Validate input file.
        """

        path = Path(input_file)

        if not path.exists():
            raise FileNotFoundError(path)

        if not path.is_file():
            raise AudioConversionError(
                "Input path is not a file."
            )

        AudioFormatRegistry.from_extension(
            path.suffix
        )

        return path

    @staticmethod
    def validate_output(
        output_file: str | Path,
    ) -> Path:
        """
        Validate output file.
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
        input_file: str | Path,
        output_file: str | Path,
    ) -> ConversionRequest:
        """
        Create validated request.
        """

        request = ConversionRequest(
            input_file=self.validate_input(
                input_file,
            ),
            output_file=self.validate_output(
                output_file,
            ),
        )

        logger.info(
            "Conversion request created."
        )

        return request
            def convert(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:
        """
        Convert audio using FFmpeg (via pydub).
        """

        request = self.create_request(
            input_file=input_file,
            output_file=output_file,
        )

        try:

            logger.info(
                "Loading audio: %s",
                request.input_file.name,
            )

            audio = AudioSegment.from_file(
                request.input_file,
            )

            export_format = (
                AudioFormatRegistry
                .from_extension(
                    request.output_file.suffix,
                )
                .value
            )

            logger.info(
                "Export format: %s",
                export_format,
            )

            audio.export(
                request.output_file,
                format=export_format,
            )

            if (
                not request.output_file.exists()
                or request.output_file.stat().st_size == 0
            ):
                raise AudioConversionError(
                    "Output file was not created."
                )

            logger.info(
                "Conversion completed successfully."
            )

            return request.output_file

        except Exception as exc:

            logger.exception(
                "Audio conversion failed."
            )

            raise AudioConversionError(
                str(exc)
            ) from exc

    def convert_to_mp3(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:

        return self.convert(
            input_file,
            output_file,
        )

    def convert_to_wav(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:

        return self.convert(
            input_file,
            output_file,
        )

    def convert_to_flac(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:

        return self.convert(
            input_file,
            output_file,
        )

    def convert_to_ogg(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:

        return self.convert(
            input_file,
            output_file,
        )

    def convert_to_m4a(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:

        return self.convert(
            input_file,
            output_file,
        )    def batch_convert(
        self,
        files: list[str | Path],
        output_directory: str | Path,
        output_format: str,
    ) -> list[Path]:
        """
        Convert multiple audio files.
        """

        output_dir = Path(output_directory)
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        registry_format = AudioFormatRegistry.validate(
            output_format,
        )

        results: list[Path] = []

        for file in files:

            source = Path(file)

            destination = (
                output_dir
                / f"{source.stem}.{registry_format.value}"
            )

            results.append(
                self.convert(
                    source,
                    destination,
                )
            )

        logger.info(
            "Batch conversion completed (%s file(s)).",
            len(results),
        )

        return results

    @staticmethod
    def verify_output(
        output_file: str | Path,
    ) -> bool:
        """
        Verify output file.
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
        Return output file size.
        """

        return Path(output_file).stat().st_size

    def health_check(
        self,
        output_file: str | Path,
    ) -> dict[str, object]:
        """
        Converter health report.
        """

        path = Path(output_file)

        return {
            "exists": path.exists(),
            "verified": self.verify_output(path),
            "size": (
                self.file_size(path)
                if path.exists()
                else 0
            ),
            "extension": path.suffix.lower(),
            "status": "healthy",
        }


audio_converter = AudioConverter()