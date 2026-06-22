import json
import asyncio
import re
from collections.abc import AsyncIterator
from unittest import result
from unittest import result
from urllib import response
from app.core.llm import OllamaClient
from app.router.prompts import ROUTER_SYSTEM_PROMPT
from app.core import config 
from app.router.plugin_router import (
    plugin_router,
)
from app.formatter.result_formatter import (
    result_formatter,
)
from app.router.execution_planner import (
    execution_planner,
)

from app.mcp.mcp_tool_runner import (
    mcp_tool_runner,
)
ROUTER_MODEL = config.ROUTER_MODEL
MODEL_MAPPING = config.WORKER_MODELS

class RoutingEngine:
    def __init__(self):
        self.client = OllamaClient()
        self.queue_lock = asyncio.Lock()
        
        self.active_queues = {model: 0 for model in set(list(MODEL_MAPPING.values()) + [ROUTER_MODEL])}
        self.ROUTER_QUEUE_LIMIT = 5

    async def _increment_queue(self, model: str):
        async with self.queue_lock:
            if model in self.active_queues:
                self.active_queues[model] += 1
            else:
                self.active_queues[model] = 1

    async def _decrement_queue(self, model: str):
        async with self.queue_lock:
            if model in self.active_queues and self.active_queues[model] > 0:
                self.active_queues[model] -= 1
    
    def _fast_keyword_fallback(self, user_input: str) -> str:
        text = user_input.lower()
        if re.search(r'\b(python|c\+\+|java|script|code|debug|function|node\.js)\b', text):
            return "Coding"
        elif re.search(r'\b(solve|math|calculate|riddle|why|how does)\b', text):
            return "Reasoning"
        elif re.search(r'\b(image|picture|look at|png|jpg|describe this)\b', text):
            return "Vision"
        return "General"

    def _is_route_trusted(self, parsed_response: dict) -> bool:
        confidence = parsed_response.get("confidence_score", 0)
        recommended = parsed_response.get("recommended", "")
        primary_prob = parsed_response.get("probabilities", {}).get(recommended, 0.0)
        return confidence >= 85 and primary_prob >= 70.0
    
    async def process_stream(self, messages: list) -> AsyncIterator[str]:
        if not messages:
            yield "Input was empty. Please provide a query."
            return

        user_input = messages[-1].get("content", "")
        route = (
            plugin_router.route(
                user_input
            )
        )

        if (
            route.get("type")
            in [
                "plugin",
                "multi_plugin",
                "cross_repo_plugin",
            ]
        ):

            plan = (
                execution_planner
                .create_plan(
                    route
                )
            )

            result = await (
                mcp_tool_runner.run(
                    plan
                )
            )

            yield (
                result_formatter
                .format(result)
            )

            return
        target_category = "General"
        is_trusted = False
        parsed_response = {}
        strategy_used = "Unknown"

        async with self.queue_lock:
            current_router_load = self.active_queues.get(ROUTER_MODEL, 0)

        if current_router_load >= self.ROUTER_QUEUE_LIMIT:
            print(f"⚠️ [LOAD SHEDDING] Router queue overloaded ({current_router_load}). Using Regex.")
            target_category = self._fast_keyword_fallback(user_input)
            strategy_used = "Load-Shedding-Regex"
            is_trusted = True 
            parsed_response = {"recommended": target_category, "confidence_score": 100}
        else:
            await self._increment_queue(ROUTER_MODEL)
            try:
                # Add router system prompt
                route_history = [{"role": "system", "content": ROUTER_SYSTEM_PROMPT}]
                route_history.extend([m for m in messages if m["role"] != "system"][-3:])
                
                raw_json_output = await self.client.generate_route(route_history)
                parsed_response = json.loads(raw_json_output)
                
                probabilities = parsed_response.get("probabilities", {})
                if probabilities:
                    target_category = max(probabilities, key=probabilities.get)
                    parsed_response["recommended"] = target_category
                else:
                    raise ValueError("Probabilities matrix missing.")

                is_trusted = self._is_route_trusted(parsed_response)
                strategy_used = "Standard-LLM-Route"
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️ [PARSE ERROR] Router failed JSON generation. Falling back to Regex. Error: {e}")
                target_category = self._fast_keyword_fallback(user_input)
                strategy_used = "Fallback-Parse-Error"
                is_trusted = True
            finally:
                await self._decrement_queue(ROUTER_MODEL)

        if strategy_used == "Standard-LLM-Route" and target_category == "General" and is_trusted and parsed_response.get("response"):
            yield parsed_response["response"]
            return
            
        elif strategy_used == "Standard-LLM-Route" and not is_trusted:
            yield "I am not entirely confident how to handle this request. Could you clarify if you are asking for coding help, general reasoning, or something else?"
            return

        else:
            fallback_model = MODEL_MAPPING.get("General", "qwen3.5:latest")
            target_model = MODEL_MAPPING.get(target_category, fallback_model)
            print(f"\n[Dispatch] Routing {target_category} task to {target_model}...")
            
            worker_history = [msg for msg in messages if msg["role"] != "system"]
            worker_prompts = {
                "Coding": "You are an expert software engineer. Provide clean, optimized, well-commented code.",
                "Reasoning": "You are an advanced logic engine. Break down problems step-by-step to find exact solutions.",
                "Vision": "You are an advanced computer vision assistant.",
                "General": "You are a highly capable AI assistant."
            }
            chosen_prompt = worker_prompts.get(target_category, "You are a helpful assistant.")
            worker_history.insert(0, {"role": "system", "content": chosen_prompt})

            await self._increment_queue(target_model)
            try:
                async for token in self.client.generate_worker_response_stream(target_model, worker_history):
                    yield token
            except Exception as e:
                print(f"\n❌ [CRITICAL ERROR] Worker {target_model} crashed: {str(e)}")
                
                if target_model != fallback_model:
                    print(f"⚠️ Executing Direct Pass-Through to {fallback_model}...")
                    await self._increment_queue(fallback_model)
                    try:
                        async for token in self.client.generate_worker_response_stream(fallback_model, worker_history):
                            yield token
                    except Exception as fallback_error:
                        yield f"System Error: Both primary and fallback models failed. Details: {str(fallback_error)}"
                    finally:
                        await self._decrement_queue(fallback_model)
                else:
                    yield f"System Error: Primary general model failed. Details: {str(e)}"
            finally:
                await self._decrement_queue(target_model)
