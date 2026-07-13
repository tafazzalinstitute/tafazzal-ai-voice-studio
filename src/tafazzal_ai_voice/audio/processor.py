"""
Production Audio Processing Pipeline.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pydub import AudioSegment

from tafazzal_ai_voice.audio.audio_processor import (
    AudioMetadata,
    AudioProcessor,
)
from tafazzal_ai_voice.audio.converter import (
    AudioConverter,
)
from tafazzal_ai_voice.audio.exporter import (
    AudioExporter,
)
from tafazzal_ai_voice.logging.logger import logger


class AudioPipelineError(Exception):
    """Raised when pipeline processing fails."""


@dataclass(slots=True)
class ProcessingRequest:
    """
    Audio processing request.
    """

    input_file: Path
    output_file: Path


class AudioPipeline:
    """
    Unified production audio pipeline.
    """

    def __init__(self) -> None:

        self.processor = AudioProcessor()

        self.converter = AudioConverter()

        self.exporter = AudioExporter()

        logger.info(
            "AudioPipeline initialized."
        )

    @staticmethod
    def create_request(
        input_file: str | Path,
        output_file: str | Path,
    ) -> ProcessingRequest:
        """
        Create processing request.
        """

        return ProcessingRequest(
            input_file=Path(input_file),
            output_file=Path(output_file),
        )

    def metadata(
        self,
        audio_file: str | Path,
    ) -> AudioMetadata:
        """
        Read audio metadata.
        """

        return self.processor.load_metadata(
            audio_file,
        )

    def load_audio(
        self,
        audio_file: str | Path,
    ) -> AudioSegment:
        """
        Load audio using pydub.
        """

        logger.info(
            "Loading audio segment."
        )

        return AudioSegment.from_file(
            audio_file,
        )    def convert(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:
        """
        Convert audio format.
        """

        logger.info(
            "Pipeline converting: %s -> %s",
            input_file,
            output_file,
        )

        return self.converter.convert(
            input_file=input_file,
            output_file=output_file,
        )

    def export(
        self,
        audio: AudioSegment,
        output_file: str | Path,
    ) -> Path:
        """
        Export audio.
        """

        logger.info(
            "Pipeline exporting audio."
        )

        return self.exporter.export(
            audio=audio,
            output_file=output_file,
        )

    def process(
        self,
        input_file: str | Path,
        output_file: str | Path,
    ) -> Path:
        """
        Complete audio processing pipeline.
        """

        request = self.create_request(
            input_file=input_file,
            output_file=output_file,
        )

        try:

            logger.info(
                "Processing started."
            )

            self.processor.validate_file(
                request.input_file,
            )

            result = self.convert(
                request.input_file,
                request.output_file,
            )

            logger.info(
                "Processing completed."
            )

            return result

        except Exception as exc:

            logger.exception(
                "Audio pipeline failed."
            )

            raise AudioPipelineError(
                str(exc)
            ) from exc
                def batch_process(
        self,
        files: list[str | Path],
        output_directory: str | Path,
        output_format: str,
    ) -> list[Path]:
        """
        Process multiple audio files.
        """

        output_dir = Path(output_directory)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        results: list[Path] = []

        for file in files:

            source = Path(file)

            destination = (
                output_dir
                / f"{source.stem}.{output_format}"
            )

            results.append(
                self.process(
                    source,
                    destination,
                )
            )

        logger.info(
            "Batch processing completed (%s file(s)).",
            len(results),
        )

        return results

    def pipeline_info(self) -> dict[str, str]:
        """
        Return pipeline information.
        """

        return {
            "name": "AudioPipeline",
            "version": "1.1",
            "status": "ready",
        }

    def health_check(
        self,
    ) -> dict[str, object]:
        """
        Pipeline health report.
        """

        return {
            "processor": "healthy",
            "converter": "healthy",
            "exporter": "healthy",
            "pipeline": "healthy",
            "info": self.pipeline_info(),
        }


audio_pipeline = AudioPipeline()