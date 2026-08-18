import os
import time

from app.services.provider_result import ProviderResult
from app.services.providers.gemini_provider import GeminiProvider
from app.services.providers.groq_provider import GroqProvider


class FallbackTutorService:

    def __init__(self):

        primary = os.getenv(
            "TUTOR_PRIMARY_PROVIDER",
            "gemini"
        ).lower()

        secondary = os.getenv(
            "TUTOR_FALLBACK_PROVIDER",
            "groq"
        ).lower()

        self.primary_name = primary
        self.secondary_name = secondary

        self.providers = {
            "gemini": GeminiProvider,
            "groq": GroqProvider,
        }

    def _create_provider(self, name):

        provider_class = self.providers.get(name)

        if not provider_class:
            raise ValueError(
                f"Unsupported provider: {name}"
            )

        return provider_class()

    def should_fallback(
        self,
        error: Exception
    ) -> bool:

        error_text = str(error).lower()

        fallback_errors = [
            "401",
            "429",
            "resource_exhausted",
            "rate limit",
            "quota",
            "timeout",
            "503",
            "service unavailable",
            "temporarily unavailable",
            "unauthenticated",
        ]

        return any(
            item in error_text
            for item in fallback_errors
        )

    def generate_response(
        self,
        message: str,
        history: list[dict],
        subject: str = "General",
    ) -> ProviderResult:

        # -------------------------
        # PRIMARY PROVIDER
        # -------------------------

        primary_provider = self._create_provider(
            self.primary_name
        )

        start_time = time.perf_counter()

        try:

            response = primary_provider.generate_response(
                message=message,
                history=history,
                subject=subject,
            )

            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            print(
                f"Provider: {self.primary_name} | "
                f"Latency: {latency_ms:.2f} ms | "
                f"Fallback: False"
            )

            return ProviderResult(
                response=response,
                provider=self.primary_name,
                fallback_used=False,
                latency_ms=latency_ms,
            )

        except Exception as primary_error:

            print(
                f"Primary provider "
                f"{self.primary_name} failed: "
                f"{primary_error}"
            )

            if not self.should_fallback(primary_error):
                raise

        # -------------------------
        # FALLBACK PROVIDER
        # -------------------------

        fallback_provider = self._create_provider(
            self.secondary_name
        )

        fallback_start = time.perf_counter()

        try:

            response = fallback_provider.generate_response(
                message=message,
                history=history,
                subject=subject,
            )

            latency_ms = (
                time.perf_counter() - fallback_start
            ) * 1000

            print(
                f"Provider: {self.secondary_name} | "
                f"Latency: {latency_ms:.2f} ms | "
                f"Fallback: True"
            )

            return ProviderResult(
                response=response,
                provider=self.secondary_name,
                fallback_used=True,
                latency_ms=latency_ms,
            )

        except Exception as fallback_error:

            print(
                f"Fallback provider "
                f"{self.secondary_name} failed: "
                f"{fallback_error}"
            )

            raise RuntimeError(
                "All AI tutor providers are unavailable."
            )