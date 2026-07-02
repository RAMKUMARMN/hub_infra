# Setup & Installation Guide

This guide covers the hardware requirements, environment setup, and execution steps for the Cixio AI Routing Engine.

## 💻 Hardware Requirements

* **GPU:** GPU with at least 8GB VRAM (e.g., RTX 4070, RTX 3060 Ti).
* **RAM:** 16GB+ System RAM.
* **Storage:** ~20GB free space for local model weights.

---

## 🚀 Installation Steps

### 1. Prerequisites
Ensure you have the following installed on your system:
* [Python 3.10+](https://www.python.org/downloads/)
* [Ollama](https://ollama.com/) (Running locally)

### 2. Pull the Local Models

```bash
ollama pull llama3.2:3b
ollama pull qwen3.5:latest
ollama pull qwen2.5-coder:7b
ollama pull llama3.2-vision:latest