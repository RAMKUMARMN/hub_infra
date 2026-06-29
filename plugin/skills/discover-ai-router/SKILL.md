---
name: discover-ai-router
description: Trace the Python FastAPI AI Router, LLM configurations, and AI payload logic.
---

# Discover AI Router

Analyze the Python-based routing engine responsible for AI request orchestration.

## Focus Areas
- FastAPI Endpoints (`ai/ai_router/app/api.py`, `main.py`)
- Engine and Prompt Configurations (`router/engine.py`, `prompts.py`)
- Core LLM integrations (`core/llm.py`)

## Goals
- Map how the infrastructure layer handles and routes AI/LLM requests.
- Verify the integration between FastAPI, the LLMs, and the MQTT message bus.

## Output
Return:
- AI Router execution flow
- Prompt and Engine configuration map

## Workflow
1. Route the hub folder agent to plugin/skills for this specific skill folder.
2. Invoke the native `discoverAiRouter` tool.
3. Map the core components inside `ai/ai_router/app/`.
4. Return the AI router architecture.
