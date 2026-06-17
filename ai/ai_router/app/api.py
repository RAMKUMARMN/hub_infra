import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from app.router.engine import RoutingEngine
from app.core.llm import OllamaClient

app = FastAPI(title="Cixio AI Router Service")

routing_engine = RoutingEngine()
ollama_client = OllamaClient()

@app.post("/api/v1/chat/stream")
async def chat_stream_endpoint(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    
    async def event_generator():
        async for token in routing_engine.process_stream(messages):
            # Format as Server-Sent Events (SSE)
            yield f"data: {json.dumps({'delta': token})}\n\n"
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")


