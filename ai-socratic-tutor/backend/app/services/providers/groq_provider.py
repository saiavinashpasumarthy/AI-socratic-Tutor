import os
import json

from dotenv import load_dotenv
from groq import Groq

from app.services.schemas import TutorResponse
from app.services.providers.base import TutorProvider


load_dotenv()


SOCRATIC_INSTRUCTION = """
You are an AI Socratic Tutor.

Your purpose is to help students develop their own
reasoning rather than simply providing answers.

Never immediately reveal the final answer unless
it is pedagogically appropriate.

Ask one useful guiding question at a time.

Evaluate the student's reasoning.

Subject:
{subject}

Guide the student through reasoning.
Do not immediately provide the complete answer.

Ask questions, identify misconceptions,
and progressively adapt your hints.

The goal is learning, not simply producing
the final answer.

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

"""
def make_strict_schema(schema):
    """
    Recursively make every object in a JSON schema
    compatible with strict structured outputs.
    """

    if isinstance(schema, dict):

        if schema.get("type") == "object":
            schema["additionalProperties"] = False

        for value in schema.values():
            make_strict_schema(value)

    elif isinstance(schema, list):

        for item in schema:
            make_strict_schema(item)

    return schema

class GroqProvider(TutorProvider):

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=api_key
        )

    def generate_response(
        self,
        message: str,
        history: list[dict],
        subject="General",
    ) -> TutorResponse:

        messages = [
            {
                "role": "system",
                "content": SOCRATIC_INSTRUCTION,
            }
        ]

        for item in history:

            role = item.get("role")
            content = item.get("content")

            if not content:
                continue

            if role == "user":
                messages.append({
                    "role": "user",
                    "content": content,
                })

            elif role == "tutor":
                messages.append({
                    "role": "assistant",
                    "content": content,
                })

        messages.append({
            "role": "user",
            "content": message,
        })

        schema = TutorResponse.model_json_schema()
        schema=make_strict_schema(schema)
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.3,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "tutor_response",
                    "strict": True,
                    "schema": schema,
                },
            },
        )

        content = response.choices[0].message.content

        data = json.loads(content)

        return TutorResponse.model_validate(data)