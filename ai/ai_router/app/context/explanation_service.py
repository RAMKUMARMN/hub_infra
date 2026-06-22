from __future__ import annotations

from app.core.llm import OllamaClient


class ExplanationService:

    def __init__(self):

        self.client = (
            OllamaClient()
        )

    async def explain(
        self,
        user_query: str,
        context: str,
    ) -> str:

        prompt = f"""
User Request:
{user_query}

Repository Context:
{context}

Explain the result clearly.

If files are present:
- explain their purpose
- explain likely relationships
- explain architecture significance

Keep response concise.
"""

        messages = [

            {
                "role": "system",
                "content":
                    "You are a senior software architect.",
            },

            {
                "role": "user",
                "content": prompt,
            },
        ]

        response = []

        async for token in (
            self.client
            .generate_worker_response_stream(
                "qwen3.5:latest",
                messages,
            )
        ):

            response.append(
                token
            )

        return "".join(
            response
        )


explanation_service = (
    ExplanationService()
)