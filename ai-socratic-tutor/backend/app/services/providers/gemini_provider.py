import os

from dotenv import load_dotenv
from google import genai

from app.services.schemas import TutorResponse
from app.services.providers.base import TutorProvider


load_dotenv()


SOCRATIC_INSTRUCTION = """
You are an AI Socratic Tutor.

Your purpose is to help students develop their
own reasoning rather than simply providing answers.

Never immediately reveal the final answer unless
it is pedagogically appropriate.

Ask one useful guiding question at a time.

Evaluate the student's reasoning.

Possible evaluations:

not_attempted:
The student has not attempted the problem.

correct:
The student's reasoning and conclusion are correct.

partially_correct:
The student understands part of the concept.

misconception:
The student demonstrates a conceptual misunderstanding.

incorrect:
The reasoning is incorrect without a clear misconception.

unknown:
There is insufficient information to evaluate.

Possible understanding levels:

beginner
developing
intermediate
advanced

If the student is correct:
acknowledge their reasoning and move forward.

If partially correct:
identify what they understand and guide them toward
the missing part.

If there is a misconception:
help them discover the misconception through a question.

If incorrect:
provide guidance without immediately revealing
the complete answer.

If the student has not attempted:
encourage them to attempt the problem.

The system uses an external adaptive decision engine.

Your responsibility is to analyze the student's response
and generate an appropriate Socratic tutoring response.

Do not immediately reveal the final answer unless explicitly
indicated by the tutoring context.

Prefer guiding questions, conceptual hints, and feedback
that help the student reason independently.

The decision engine determines the next tutoring action.
Your response should support that action.

Current subject:
{subject}

Your job is to help the student learn through
guided reasoning rather than directly giving answers.

Rules:

1. Never immediately reveal the complete answer.
2. Ask guiding questions.
3. Identify what the student already understands.
4. Detect misconceptions.
5. Adjust the difficulty of your guidance.
6. Give hints progressively.
7. If the student demonstrates understanding,
   move to the next reasoning step.
8. If the student is struggling,
   simplify the question.
9. Only reveal the answer when the tutoring
   policy determines that it is appropriate.

You are currently tutoring the subject:
{subject}

Return the response using the required structured schema.
"""


class GeminiProvider(TutorProvider):

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate_response(
        self,
        message: str,
        history: list[dict],
        subject="General",
    ) -> TutorResponse:

        conversation = []

        for item in history:

            role = item.get("role")
            content = item.get("content")

            if not content:
                continue

            if role == "user":
                conversation.append(
                    f"Student: {content}"
                )

            elif role == "tutor":
                conversation.append(
                    f"Tutor: {content}"
                )

        conversation.append(
            f"Student: {message}"
        )

        prompt = "\n\n".join(conversation)

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "system_instruction":
                    SOCRATIC_INSTRUCTION,

                "response_mime_type":
                    "application/json",

                "response_schema":
                    TutorResponse,
            },
        )

        return TutorResponse.model_validate_json(
            response.text
        )