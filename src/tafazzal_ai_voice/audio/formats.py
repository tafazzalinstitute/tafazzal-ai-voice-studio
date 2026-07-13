"""
Production-ready audio format registry.

Tafazzal AI Voice Studio
Version: 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final


class AudioFormat(str, Enum):
    """
    Supported audio formats.
    """

    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"


SUPPORTED_FORMATS: Final[frozenset[AudioFormat]] = frozenset(
    {
        AudioFormat.WAV,
        AudioFormat.MP3,
        AudioFormat.FLAC,
        AudioFormat.OGG,
        AudioFormat.M4A,
    }
)


@dataclass(frozen=True, slots=True)
class AudioFormatInfo:
    """
    Audio format metadata.
    """

    extension: str
    mime_type: str
    codec: str
    description: str


FORMAT_REGISTRY: Final[dict[AudioFormat, AudioFormatInfo]] = {
    AudioFormat.WAV: AudioFormatInfo(
        extension=".wav",
        mime_type="audio/wav",
        codec="pcm_s16le",
        description="Waveform Audio File Format",
    ),
    AudioFormat.MP3: AudioFormatInfo(
        extension=".mp3",
        mime_type="audio/mpeg",
        codec="libmp3lame",
        description="MPEG Layer III Audio",
    ),
    AudioFormat.FLAC: AudioFormatInfo(
        extension=".flac",
        mime_type="audio/flac",
        codec="flac",
        description="Free Lossless Audio Codec",
    ),
    AudioFormat.OGG: AudioFormatInfo(
        extension=".ogg",
        mime_type="audio/ogg",
        codec="libvorbis",
        description="Ogg Vorbis Audio",
    ),
    AudioFormat.M4A: AudioFormatInfo(
        extension=".m4a",
        mime_type="audio/mp4",
        codec="aac",
        description="MPEG-4 Audio",
    ),
}class AudioFormatError(Exception):
    """
    Raised when an invalid audio format is requested.
    """


class AudioFormatRegistry:
    """
    Production audio format registry.
    """

    @staticmethod
    def validate(
        audio_format: str | AudioFormat,
    ) -> AudioFormat:
        """
        Validate and return AudioFormat.
        """

        if isinstance(audio_format, AudioFormat):
            return audio_format

        try:
            return AudioFormat(audio_format.lower())

        except ValueError as exc:

            raise AudioFormatError(
                f"Unsupported audio format: {audio_format}"
            ) from exc

    @classmethod
    def info(
        cls,
        audio_format: str | AudioFormat,
    ) -> AudioFormatInfo:
        """
        Return format information.
        """

        fmt = cls.validate(audio_format)

        return FORMAT_REGISTRY[fmt]

    @classmethod
    def mime_type(
        cls,
        audio_format: str | AudioFormat,
    ) -> str:
        """
        Return MIME type.
        """

        return cls.info(audio_format).mime_type

    @classmethod
    def codec(
        cls,
        audio_format: str | AudioFormat,
    ) -> str:
        """
        Return FFmpeg codec.
        """

        return cls.info(audio_format).codec

    @classmethod
    def extension(
        cls,
        audio_format: str | AudioFormat,
    ) -> str:
        """
        Return file extension.
        """

        return cls.info(audio_format).extension

    @classmethod
    def description(
        cls,
        audio_format: str | AudioFormat,
    ) -> str:
        """
        Return format description.
        """

        return cls.info(audio_format).description
            @classmethod
    def from_extension(
        cls,
        extension: str,
    ) -> AudioFormat:
        """
        Detect format from file extension.
        """

        extension = extension.lower()

        if not extension.startswith("."):
            extension = f".{extension}"

        for fmt, info in FORMAT_REGISTRY.items():

            if info.extension == extension:
                return fmt

        raise AudioFormatError(
            f"Unknown extension: {extension}"
        )

    @classmethod
    def is_supported(
        cls,
        audio_format: str | AudioFormat,
    ) -> bool:
        """
        Check whether a format is supported.
        """

        try:
            cls.validate(audio_format)
            return True

        except AudioFormatError:
            return False

    @classmethod
    def supported_formats(
        cls,
    ) -> list[str]:
        """
        Return supported format names.
        """

        return [
            fmt.value
            for fmt in AudioFormat
        ]    @classmethod
    def default_format(cls) -> AudioFormat:
        """
        Return default audio format.
        """

        return AudioFormat.WAV

    @classmethod
    def default_codec(cls) -> str:
        """
        Return default codec.
        """

        return cls.codec(
            cls.default_format()
        )

    @classmethod
    def health_check(cls) -> dict[str, object]:
        """
        Registry health report.
        """

        return {
            "formats": len(FORMAT_REGISTRY),
            "supported": cls.supported_formats(),
            "default": cls.default_format().value,
            "default_codec": cls.default_codec(),
            "status": "healthy",
        }DEFAULT_AUDIO_FORMAT: Final[AudioFormat] = (
    AudioFormatRegistry.default_format()
)

DEFAULT_AUDIO_CODEC: Final[str] = (
    AudioFormatRegistry.default_codec()
)

audio_formats = AudioFormatRegistry()