"""
Production-ready audio exporter.

Tafazzal AI Voice Studio
Version: 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from tafazzal_ai_voice.logging.logger import logger


SUPPORTED_EXPORT_FORMATS: Final[frozenset[str]] = frozenset(
    {
        "wav",
        "mp3",
        "flac",
        "ogg",
        "m4a",
    }
)


@dataclass(slots=True)
class ExportProfile:
    """
    Audio export configuration.
    """

    format: str
    bitrate: str = "192k"
    sample_rate: int = 44100
    channels: int = 2


class AudioExportError(Exception):
    """
    Raised when export fails.
    """


class AudioExporter:
    """
    Production audio exporter.
    """

    def __init__(self) -> None:

        logger.info(
            "AudioExporter initialized."
        )

    @staticmethod
    def validate_format(
        export_format: str,
    ) -> str:
        """
        Validate export format.
        """

        export_format = export_format.lower()

        if export_format not in SUPPORTED_EXPORT_FORMATS:

            raise AudioExportError(
                f"Unsupported export format: {export_format}"
            )

        return export_format

    @staticmethod
    def validate_output(
        output_file: str | Path,
    ) -> Path:
        """
        Validate output path.
        """

        path = Path(output_file)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    def create_profile(
        self,
        export_format: str,
        bitrate: str = "192k",
        sample_rate: int = 44100,
        channels: int = 2,
    ) -> ExportProfile:
        """
        Create validated export profile.
        """

        profile = ExportProfile(
            format=self.validate_format(
                export_format,
            ),
            bitrate=bitrate,
            sample_rate=sample_rate,
            channels=channels,
        )

        logger.info(
            "Export profile created: %s",
            profile.format,
        )

        return profile    def export(
        self,
        audio,
        output_file: str | Path,
        profile: ExportProfile,
    ) -> Path:
        """
        Export audio using pydub + FFmpeg.
        """

        from pydub import AudioSegment

        if not isinstance(audio, AudioSegment):
            raise AudioExportError(
                "audio must be a pydub.AudioSegment instance."
            )

        output_path = self.validate_output(output_file)

        export_parameters: dict[str, object] = {
            "format": profile.format,
        }

        if profile.format == "mp3":
            export_parameters["bitrate"] = profile.bitrate

        try:

            processed_audio = (
                audio.set_frame_rate(profile.sample_rate)
                     .set_channels(profile.channels)
            )

            logger.info(
                "Exporting audio -> %s",
                output_path.name,
            )

            processed_audio.export(
                output_path,
                **export_parameters,
            )

            if (
                not output_path.exists()
                or output_path.stat().st_size == 0
            ):
                raise AudioExportError(
                    "Export failed. Output file is empty."
                )

            logger.info(
                "Audio exported successfully."
            )

            return output_path

        except Exception as exc:

            logger.exception(
                "Audio export failed."
            )

            raise AudioExportError(
                str(exc)
            ) from exc    def export_mp3(
        self,
        audio,
        output_file: str | Path,
        bitrate: str = "192k",
    ) -> Path:

        profile = self.create_profile(
            export_format="mp3",
            bitrate=bitrate,
        )

        return self.export(
            audio,
            output_file,
            profile,
        )


    def export_wav(
        self,
        audio,
        output_file: str | Path,
    ) -> Path:

        profile = self.create_profile(
            export_format="wav",
        )

        return self.export(
            audio,
            output_file,
            profile,
        )


    def export_flac(
        self,
        audio,
        output_file: str | Path,
    ) -> Path:

        profile = self.create_profile(
            export_format="flac",
        )

        return self.export(
            audio,
            output_file,
            profile,
        )


    def export_ogg(
        self,
        audio,
        output_file: str | Path,
    ) -> Path:

        profile = self.create_profile(
            export_format="ogg",
        )

        return self.export(
            audio,
            output_file,
            profile,
        )


    def export_m4a(
        self,
        audio,
        output_file: str | Path,
    ) -> Path:

        profile = self.create_profile(
            export_format="m4a",
        )

        return self.export(
            audio,
            output_file,
            profile,
        )    def batch_export(
        self,
        audio,
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

        results: list[Path] = []

        for export_format in formats:

            output_file = (
                output_dir /
                f"{base_name}.{export_format.lower()}"
            )

            profile = self.create_profile(
                export_format=export_format,
            )

            results.append(
                self.export(
                    audio=audio,
                    output_file=output_file,
                    profile=profile,
                )
            )

        logger.info(
            "Batch export completed (%s file(s)).",
            len(results),
        )

        return results

    @staticmethod
    def verify_output(
        output_file: str | Path,
    ) -> bool:
        """
        Verify exported file.
        """

        path = Path(output_file)

        return (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
        )

    @staticmethod
    def export_profiles() -> dict[str, ExportProfile]:
        """
        Built-in export profiles.
        """

        return {
            "youtube": ExportProfile(
                format="mp3",
                bitrate="320k",
                sample_rate=48000,
                channels=2,
            ),
            "podcast": ExportProfile(
                format="mp3",
                bitrate="192k",
                sample_rate=44100,
                channels=2,
            ),
            "studio": ExportProfile(
                format="wav",
                sample_rate=48000,
                channels=2,
            ),
        }

    def health_check(
        self,
        output_file: str | Path,
    ) -> dict[str, object]:
        """
        Export health report.
        """

        path = Path(output_file)

        return {
            "exists": path.exists(),
            "verified": self.verify_output(path),
            "size": (
                path.stat().st_size
                if path.exists()
                else 0
            ),
            "extension": path.suffix.lower(),
        }


audio_exporter = AudioExporter()