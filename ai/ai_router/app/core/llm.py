import httpx
import json
from collections.abc import AsyncIterator
from app.core import config

class OllamaClient:
    def __init__(self):
        self.chat_url = config.LLM_CHAT_ENDPOINT
        self.model = config.ROUTER_MODEL

        self.schema = {
            "type": "object",
            "properties": {
                "confidence_score": {"type": "integer"},
                "probabilities": {
                    "type": "object",
                    "properties": {
                        "General": {"type": "number"},
                        "Reasoning": {"type": "number"},
                        "Coding": {"type": "number"},
                        "Vision": {"type": "number"}
                    },
                    "required": ["General", "Reasoning", "Coding", "Vision"]
                },
                "response": {"type": "string"}
            },
            "required": ["confidence_score", "probabilities", "response"]
        }

    async def generate_route(self, messages: list) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "format": self.schema,
            "keep_alive": -1
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.chat_url, json=payload)
                response.raise_for_status()
                return response.json().get("message", {}).get("content", "{}")
        except Exception as e:
            return f'{{"error": "Failed to reach LLM endpoint at {self.chat_url}: {str(e)}"}}'
    
    async def generate_worker_response_stream(self, target_model: str, messages: list) -> AsyncIterator[str]:
        """Queries the specialized worker models and yields the output in real-time."""
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": True,
            "keep_alive": "5m",
            "options": {
                "num_ctx": 4096,
                "num_predict": 2048
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", self.chat_url, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            if content:
                                yield content
        except Exception as e:
            yield f" Worker model ({target_model}) failed: {str(e)}"
