from dataclasses import dataclass, field


@dataclass
class TutorSessionState:

    topic: str = ""

    current_hint_level: int = 0

    attempts: int = 0

    misconceptions: list[str] = field(
        default_factory=list
    )

    last_evaluation: str = "not_attempted"

    last_action: str = "guide"

    solved: bool = False
class SessionStateManager:

    def __init__(self):

        self.sessions: dict[str, TutorSessionState] = {}

    def get_session(
        self,
        session_id: str,
    ) -> TutorSessionState:

        if session_id not in self.sessions:

            self.sessions[session_id] = (
                TutorSessionState()
            )

        return self.sessions[session_id]

    def update_session(
        self,
        session_id: str,
        evaluation: str,
        action: str,
        hint_level: int,
        misconception: str | None = None,
    ) -> TutorSessionState:

        session = self.get_session(session_id)

        session.attempts += 1

        session.last_evaluation = evaluation

        session.last_action = action

        session.current_hint_level = hint_level

        if evaluation == "correct":
            session.solved = True

        if misconception:
            if misconception not in session.misconceptions:
                session.misconceptions.append(
                    misconception
                )

        return session

    def reset_session(
        self,
        session_id: str,
    ):

        self.sessions[session_id] = (
            TutorSessionState()
        )

        return self.sessions[session_id]
session_manager = SessionStateManager()