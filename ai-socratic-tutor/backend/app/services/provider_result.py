from dataclasses import dataclass

from app.services.schemas import TutorResponse


@dataclass
class ProviderResult:

    response: TutorResponse

    provider: str

    fallback_used: bool

    latency_ms: float