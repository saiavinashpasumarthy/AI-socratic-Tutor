import os

from app.services.providers.base import TutorProvider
from app.services.providers.gemini_provider import GeminiProvider
from app.services.providers.groq_provider import GroqProvider


def get_tutor_provider() -> TutorProvider:

    provider = os.getenv(
        "TUTOR_PROVIDER",
        "gemini",
    ).lower()

    if provider == "gemini":
        return GeminiProvider()

    if provider == "groq":
        return GroqProvider()

    raise ValueError(
        f"Unsupported tutor provider: {provider}"
    )