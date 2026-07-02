import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

LLM_CHAT_ENDPOINT = os.getenv("LLM_CHAT_ENDPOINT", "http://localhost:11434/api/chat")
ROUTER_MODEL = os.getenv("ROUTER_MODEL", "llama3.2:3b")

# Map the categories to the environment variables
WORKER_MODELS = {
    "General": os.getenv("MODEL_GENERAL", "qwen3.5:latest"),
    "Coding": os.getenv("MODEL_CODING", "qwen2.5-coder:7b"),
    "Reasoning": os.getenv("MODEL_REASONING", "qwen3.5:latest"),
    "Vision": os.getenv("MODEL_VISION", "llama3.2-vision:latest"),
    
    # Fallbacks handled by the router itself
    "Clarification Needed": ROUTER_MODEL,
    "Error": ROUTER_MODEL
}