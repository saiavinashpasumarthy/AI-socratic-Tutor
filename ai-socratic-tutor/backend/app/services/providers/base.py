from abc import ABC, abstractmethod

from app.services.schemas import TutorResponse


class TutorProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        message: str,
        history: list[dict],
        subject="General",
    ) -> TutorResponse:
        raise NotImplementedError