#!/bin/bash
set -e

echo "==========================================================="
echo "🚀 Starting CixioHub Infrastructure (Docker)"
echo "==========================================================="

# 1. Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed. Please install Docker and Docker Compose."
    exit 1
fi

# 2. Build and start services
echo -e "\n📦 Building and starting containers (Ollama, AI Router)..."
docker compose up -d --build

# 3. Wait for models to pull
echo -e "\n📥 Waiting for Ollama models to be pulled (this depends on your internet speed)..."
echo "You can safely press Ctrl+C to detach from these logs at any time."
docker compose logs -f ollama-pull || true

# 4. Provide instructions
echo -e "\n✅ Infrastructure setup complete!"
echo "The AI Router simulator is running in the background with TTY enabled."
echo ""
echo "👉 To interact with the AI Router, run:"
echo "   docker attach cixiohub-ai_router"
echo ""
echo "💡 Important: To detach from the router without stopping the container, press 'Ctrl+P' then 'Ctrl+Q'."
echo "==========================================================="
