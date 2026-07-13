"""
Production Voice Registry.

Tafazzal AI Voice Studio
Version 1.1
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final


class VoiceProvider(str, Enum):
    """
    Supported AI providers.
    """

    GOOGLE = "google"
    OPENAI = "openai"


class VoiceGender(str, Enum):
    """
    Voice gender.
    """

    MALE = "male"
    FEMALE = "female"


class VoiceLanguage(str, Enum):
    """
    Supported languages.
    """

    BANGLA = "bn"
    ENGLISH = "en"


@dataclass(frozen=True, slots=True)
class VoiceProfile:
    """
    Voice profile definition.
    """

    name: str
    provider: VoiceProvider
    language: VoiceLanguage
    gender: VoiceGender
    description: str


VOICE_REGISTRY: Final[dict[str, VoiceProfile]] = {

    "google_bn_male": VoiceProfile(
        name="Bangla Male",
        provider=VoiceProvider.GOOGLE,
        language=VoiceLanguage.BANGLA,
        gender=VoiceGender.MALE,
        description="Google Bangla Male Voice",
    ),

    "google_bn_female": VoiceProfile(
        name="Bangla Female",
        provider=VoiceProvider.GOOGLE,
        language=VoiceLanguage.BANGLA,
        gender=VoiceGender.FEMALE,
        description="Google Bangla Female Voice",
    ),

    "google_en_male": VoiceProfile(
        name="English Male",
        provider=VoiceProvider.GOOGLE,
        language=VoiceLanguage.ENGLISH,
        gender=VoiceGender.MALE,
        description="Google English Male Voice",
    ),

    "google_en_female": VoiceProfile(
        name="English Female",
        provider=VoiceProvider.GOOGLE,
        language=VoiceLanguage.ENGLISH,
        gender=VoiceGender.FEMALE,
        description="Google English Female Voice",
    ),

    "openai_bn_male": VoiceProfile(
        name="Bangla Male",
        provider=VoiceProvider.OPENAI,
        language=VoiceLanguage.BANGLA,
        gender=VoiceGender.MALE,
        description="OpenAI Bangla Male Voice",
    ),

    "openai_en_female": VoiceProfile(
        name="English Female",
        provider=VoiceProvider.OPENAI,
        language=VoiceLanguage.ENGLISH,
        gender=VoiceGender.FEMALE,
        description="OpenAI English Female Voice",
    ),
}class VoiceRegistryError(Exception):
    """
    Raised when an invalid voice is requested.
    """


class VoiceRegistry:
    """
    Unified production voice registry.
    """

    @staticmethod
    def validate(
        voice_id: str,
    ) -> VoiceProfile:
        """
        Validate voice id.
        """

        key = voice_id.lower()

        if key not in VOICE_REGISTRY:

            raise VoiceRegistryError(
                f"Unknown voice: {voice_id}"
            )

        return VOICE_REGISTRY[key]

    @classmethod
    def get(
        cls,
        voice_id: str,
    ) -> VoiceProfile:
        """
        Return voice profile.
        """

        return cls.validate(
            voice_id,
        )

    @classmethod
    def by_provider(
        cls,
        provider: VoiceProvider,
    ) -> list[VoiceProfile]:
        """
        Return voices by provider.
        """

        return [
            profile
            for profile in VOICE_REGISTRY.values()
            if profile.provider == provider
        ]

    @classmethod
    def by_language(
        cls,
        language: VoiceLanguage,
    ) -> list[VoiceProfile]:
        """
        Return voices by language.
        """

        return [
            profile
            for profile in VOICE_REGISTRY.values()
            if profile.language == language
        ]

    @classmethod
    def by_gender(
        cls,
        gender: VoiceGender,
    ) -> list[VoiceProfile]:
        """
        Return voices by gender.
        """

        return [
            profile
            for profile in VOICE_REGISTRY.values()
            if profile.gender == gender
        ]

    @classmethod
    def default_voice(
        cls,
    ) -> VoiceProfile:
        """
        Return default voice.
        """

        return VOICE_REGISTRY[
            "google_bn_male"
        ]    @classmethod
    def voice_ids(
        cls,
    ) -> list[str]:
        """
        Return all registered voice IDs.
        """

        return sorted(
            VOICE_REGISTRY.keys()
        )

    @classmethod
    def providers(
        cls,
    ) -> list[str]:
        """
        Return supported providers.
        """

        return [
            provider.value
            for provider in VoiceProvider
        ]

    @classmethod
    def languages(
        cls,
    ) -> list[str]:
        """
        Return supported languages.
        """

        return [
            language.value
            for language in VoiceLanguage
        ]

    @classmethod
    def health_check(
        cls,
    ) -> dict[str, object]:
        """
        Voice registry health report.
        """

        return {
            "voices": len(VOICE_REGISTRY),
            "providers": cls.providers(),
            "languages": cls.languages(),
            "default_voice": cls.default_voice().name,
            "status": "healthy",
        }


DEFAULT_VOICE: Final[VoiceProfile] = (
    VoiceRegistry.default_voice()
)

voice_registry = VoiceRegistry()