# Cixio AI Routing Engine

A high-performance, self-healing, and context-aware local AI routing system. This engine acts as the core intelligence of the Cixio infrastructure. It dynamically intercepts user queries, classifies intent using a lightning-fast lightweight LLM, and dispatches complex workloads to specialized, heavy-parameter worker models.

Designed to run locally on consumer hardware (specifically optimized for 8GB VRAM environments like the RTX 4070), it guarantees zero-latency conversational routing while preserving deep reasoning and low-level coding capabilities.

*For setup and execution instructions, please see [INSTALLATION.md](INSTALLATION.md).*

---

## 🧠 Architecture Overview

The system utilizes a specialized **Two-Tier LLM Architecture**:

### 1. The Fast Path (The Router)
* **Default Model:** `llama3.2:3b ` (Recommended for strict JSON) or `qwen2.5:1.5b`.
* **Role:** The Traffic Cop. It analyzes the prompt, assigns a confidence score, and calculates a strict probability matrix across four categories (`General`, `Reasoning`, `Coding`, `Vision`).
* **Execution:** If the router's confidence hits the Double-Lock Threshold (Score >= 85 AND Probability >= 70%), and the task is casual `General` chat, it serves its own response instantly without waking up the heavy models.

### 2. The Escalation Path (The Workers)
* **Worker Models:** `qwen2.5-coder:7b` (Coding), `qwen3.5:latest` (Reasoning), `llama3.2-vision:latest` (Vision).
* **Role:** The Heavy Lifters.
* **Execution:** If the router's confidence drops, or the task requires specialized skills (e.g., C/C++ programming, complex algorithms), the Python engine dynamically unloads the router from VRAM, loads the specialized worker, and streams the deep-reasoning response token-by-token.

---

## ✨ Key Features

* **Deterministic Routing:** Python calculates the winning categories, preventing small-model string hallucinations.
* **Double-Lock Safety Threshold:** Prevents the "Confidently Wrong" AI problem by cross-referencing self-reported confidence scores with category probabilities.
* **Semantic Hijack Protection:** System prompts are strictly sandboxed and scrubbed during model handoffs to prevent context contamination.
* **Aggressive VRAM Optimization:** Utilizes `keep_alive: 0` swaps to ensure 8GB GPUs can seamlessly transition between the router and an 8GB context-heavy worker without throwing `500 Internal Server Errors`.
* **Real-Time Streaming:** Uses `httpx` to stream long-form worker outputs instantly to the terminal/UI.

---

## 🗺️ Next Steps / Roadmap

* **Network Ingress:** Integrate `paho-mqtt` to allow the engine to listen for JSON payloads over the Mosquitto broker (`cixio/router/request`).
* **Knowledge Base (RAG):** Connect a local vector database to allow worker models to read local file structures and PDF documents.