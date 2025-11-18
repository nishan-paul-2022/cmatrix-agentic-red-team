import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import asyncio
import importlib

load_dotenv()

app = FastAPI(
    title="DeepHat Agent API",
    description="AI Agent with LangGraph and tool calling",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list = []

class ChatResponse(BaseModel):
    response: str

def get_agent():
    """Dynamically import orchestrator to support hot reloading."""
    import orchestrator
    importlib.reload(orchestrator)
    return orchestrator.run_orchestrator

@app.get("/")
async def root():
    return {
        "message": "DeepHat Agent API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "stream": "/chat/stream"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "DeepHat Agent API"
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint."""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        run_agent = get_agent()
        response = run_agent(request.message, request.history)
        return ChatResponse(response=response)
    
    except Exception as e:
        print(f"Error in /chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint."""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        async def generate():
            try:
                run_agent = get_agent()
                response = run_agent(request.message, request.history)

                if not response:
                    yield f"data: {json.dumps({'error': 'Empty response from agent'})}\n\n"
                    return

                # Check if response is a dict with animation steps (demo mode)
                if isinstance(response, dict) and "animation_steps" in response:
                    animation_steps = response["animation_steps"]
                    final_answer = response["final_answer"]
                    diagram_data = response.get("diagram")

                    print(f'📤 Streaming DEMO response with {len(animation_steps)} steps')

                    # First, send diagram data if available
                    if diagram_data:
                        yield f"data: {json.dumps({'diagram': diagram_data})}\n\n"

                    # Then send animation steps
                    for step in animation_steps:
                        yield f"data: {json.dumps({'animation_step': step})}\n\n"
                        await asyncio.sleep(step["duration"] / 1000)  # Convert ms to seconds

                    # Then stream the final answer
                    words = final_answer.split()
                    newline_token = '\n'
                    for i, word in enumerate(words):
                        # Preserve line breaks
                        if newline_token in word:
                            parts = word.split(newline_token)
                            for j, part in enumerate(parts):
                                if part:
                                    yield f"data: {json.dumps({'token': part})}\n\n"
                                if j < len(parts) - 1:
                                    yield f"data: {json.dumps({'token': newline_token})}\n\n"
                        else:
                            chunk = word + (" " if i < len(words) - 1 else "")
                            yield f"data: {json.dumps({'token': chunk})}\n\n"

                        await asyncio.sleep(0.03)  # Slightly faster streaming

                else:
                    # Regular streaming for non-demo responses
                    print(f'📤 Streaming regular response ({len(response)} chars)')

                    # Stream by words for better readability
                    words = response.split()
                    newline_token = '\n'
                    for i, word in enumerate(words):
                        # Preserve line breaks
                        if newline_token in word:
                            parts = word.split(newline_token)
                            for j, part in enumerate(parts):
                                if part:
                                    yield f"data: {json.dumps({'token': part})}\n\n"
                                if j < len(parts) - 1:
                                    yield f"data: {json.dumps({'token': newline_token})}\n\n"
                        else:
                            chunk = word + (" " if i < len(words) - 1 else "")
                            yield f"data: {json.dumps({'token': chunk})}\n\n"

                        await asyncio.sleep(0.03)  # Slightly faster streaming

                yield "data: [DONE]\n\n"
            
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Error in /chat/stream: {error_msg}")
                import traceback
                traceback.print_exc()
                
                # Provide user-friendly error messages
                if "Model is loading" in error_msg or "503" in error_msg:
                    user_msg = "The AI model is currently loading. Please wait a moment and try again."
                elif "timeout" in error_msg.lower():
                    user_msg = "Request timed out. Please try again."
                elif "401" in error_msg or "403" in error_msg:
                    user_msg = "Authentication error. Please check your API key."
                else:
                    user_msg = f"An error occurred: {error_msg}"
                
                yield f"data: {json.dumps({'error': user_msg})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        print(f"❌ Error in /chat/stream endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting DeepHat Agent API on port {port}")
    print(f"📝 Hot reload enabled - code changes will auto-reload")
    print(f"🔗 API docs available at http://localhost:{port}/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["./"],
        log_level="info"
    )
