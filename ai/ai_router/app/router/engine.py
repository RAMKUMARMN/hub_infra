import json
import threading
import re
from app.core.llm import OllamaClient
from app.router.prompts import ROUTER_SYSTEM_PROMPT
from app.core import config # Ensure this is imported if you use config variables

# Mirroring your environment mapping
ROUTER_MODEL = "llama3.2:3b"
MODEL_MAPPING = {
    "General": "qwen3.5:latest",
    "Coding": "qwen2.5-coder:7b",
    "Reasoning": "qwen3.5:latest",
    "Vision": "llama3.2-vision:latest"
}

class RoutingEngine:
    def __init__(self):
        self.client = OllamaClient()
        self.sessions = {}
        self.queue_lock = threading.Lock()
        
        # Track active requests inside your Python gateway
        self.active_queues = {
            ROUTER_MODEL: 0,
            "qwen3.5:latest": 0,
            "qwen2.5-coder:7b": 0,
            "llama3.2-vision:latest": 0
        }
        
        # Safety circuit-breaker threshold
        self.ROUTER_QUEUE_LIMIT = 5

    def _increment_queue(self, model: str):
        with self.queue_lock:
            if model in self.active_queues:
                self.active_queues[model] += 1

    def _decrement_queue(self, model: str):
        with self.queue_lock:
            if model in self.active_queues and self.active_queues[model] > 0:
                self.active_queues[model] -= 1
                
    def _fast_keyword_fallback(self, user_input: str) -> str:
        """Stage 1 Defense: Pure localized string matching (0.00ms execution)"""
        text = user_input.lower()
        if re.search(r'\b(python|c\+\+|java|script|code|debug|function|node\.js)\b', text):
            return "Coding"
        elif re.search(r'\b(solve|math|calculate|riddle|why|how does)\b', text):
            return "Reasoning"
        elif re.search(r'\b(image|picture|look at|png|jpg|describe this)\b', text):
            return "Vision"
        return "General"

    def get_or_create_session(self, session_id: str) -> list:
        if session_id not in self.sessions:
            self.sessions[session_id] = [
                {"role": "system", "content": ROUTER_SYSTEM_PROMPT}
            ]
        return self.sessions[session_id]

    def _is_route_trusted(self, parsed_response: dict) -> bool:
        confidence = parsed_response.get("confidence_score", 0)
        recommended = parsed_response.get("recommended", "")
        primary_prob = parsed_response.get("probabilities", {}).get(recommended, 0.0)
        return confidence >= 85 and primary_prob >= 70.0

    def process_query(self, session_id: str, user_input: str) -> dict:
        # 1. Input Guardrail
        if not user_input or not user_input.strip():
            return self._fallback_error("Input was empty. Please provide a query.")

        history = self.get_or_create_session(session_id)
        history.append({"role": "user", "content": user_input})
        
        target_category = "General"
        is_trusted = False
        parsed_response = {}
        strategy_used = "Unknown"

        # ==========================================
        # PHASE 1: ROUTING (LLM or Regex)
        # ==========================================
        with self.queue_lock:
            current_router_load = self.active_queues[ROUTER_MODEL]

        if current_router_load >= self.ROUTER_QUEUE_LIMIT:
            # LOAD SHEDDING ENGAGED: Bypass Router LLM
            print(f"⚠️ [LOAD SHEDDING] Router queue overloaded ({current_router_load}). Using Regex.")
            target_category = self._fast_keyword_fallback(user_input)
            strategy_used = "Load-Shedding-Regex"
            is_trusted = True # We trust our regex in an emergency
            parsed_response = {"recommended": target_category, "confidence_score": 100}
        else:
            # NORMAL ROUTING: Use Llama 3.2 3B
            self._increment_queue(ROUTER_MODEL)
            try:
                raw_json_output = self.client.generate_route(history)
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
                # Fallback if the router outputs corrupt JSON
                print(f"⚠️ [PARSE ERROR] Router failed JSON generation. Falling back to Regex.")
                target_category = self._fast_keyword_fallback(user_input)
                strategy_used = "Fallback-Parse-Error"
                is_trusted = True
            finally:
                self._decrement_queue(ROUTER_MODEL)

        # ==========================================
        # PHASE 2: EXECUTION (Worker or Fast Path)
        # ==========================================
        final_answer = ""
        target_model = "Unknown"

        # CASE A: Fast Path (Router successfully handled General Chat)
        if strategy_used == "Standard-LLM-Route" and target_category == "General" and is_trusted and parsed_response.get("response"):
            target_model = ROUTER_MODEL
            final_answer = parsed_response["response"]
            
        # CASE B: Clarification Needed
        elif strategy_used == "Standard-LLM-Route" and not is_trusted:
            target_model = ROUTER_MODEL
            target_category = "Clarification Needed"
            final_answer = "I am not entirely confident how to handle this request. Could you clarify if you are asking for coding help, general reasoning, or something else?"

        # CASE C: Worker Dispatch (Escalation OR Load-Shedded General)
        else:
            # Map the category to the correct heavy model
            target_model = MODEL_MAPPING.get(target_category, "qwen3.5:latest")
            print(f"\n\033[33m[Dispatch]\033[0m Routing {target_category} task to {target_model}...")
            
            # Setup worker context
            worker_history = [msg for msg in history if msg["role"] != "system"]
            worker_prompts = {
                "Coding": "You are an expert software engineer. Provide clean, optimized, well-commented code.",
                "Reasoning": "You are an advanced logic engine. Break down problems step-by-step to find exact solutions.",
                "Vision": "You are an advanced computer vision assistant.",
                "General": "You are a highly capable AI assistant."
            }
            chosen_prompt = worker_prompts.get(target_category, "You are a helpful assistant.")
            worker_history.insert(0, {"role": "system", "content": chosen_prompt})

            # Execute with Queue Tracking & 500 Error Protection
            self._increment_queue(target_model)
            try:
                final_answer = self.client.generate_worker_response(target_model, worker_history)
            except Exception as e:
                print(f"\n❌ [CRITICAL ERROR] Worker {target_model} crashed: {str(e)}")
                
                # STAGE 2 DEFENSE: Direct Pass-Through Fallback
                if target_model != "qwen3.5:latest":
                    print(f"⚠️ Executing Direct Pass-Through to qwen3.5:latest...")
                    self._increment_queue("qwen3.5:latest")
                    try:
                        final_answer = self.client.generate_worker_response("qwen3.5:latest", worker_history)
                        target_model = "qwen3.5:latest (EMERGENCY PASS-THROUGH)"
                    except Exception as fallback_error:
                        final_answer = f"System Error: Both primary and fallback models failed. Details: {str(fallback_error)}"
                    finally:
                        self._decrement_queue("qwen3.5:latest")
                else:
                    final_answer = f"System Error: Primary general model failed. Details: {str(e)}"
            finally:
                self._decrement_queue(target_model)

        # ==========================================
        # FINALIZATION
        # ==========================================
        parsed_response["target_model"] = target_model
        parsed_response["recommended"] = target_category
        parsed_response["response"] = final_answer
        parsed_response["strategy"] = strategy_used
        
        # Save to memory
        history.append({"role": "assistant", "content": final_answer})
        
        return parsed_response

    def _fallback_error(self, message: str) -> dict:
        return {
            "confidence_score": 0,
            "probabilities": {"General": 100.0},
            "recommended": "Error",
            "target_model": ROUTER_MODEL,
            "response": message,
            "strategy": "System-Error"
        }