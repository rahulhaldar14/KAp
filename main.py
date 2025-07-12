from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Kokoro-FastAPI Streaming Server"}

@app.get("/stream")
async def video_stream():
    async def generate_frames():
        # Replace with your actual streaming logic
        for i in range(100):
            yield f"data: Frame {i}\n\n"
            await asyncio.sleep(0.05)  # ~20 FPS streaming
    
    return StreamingResponse(
        generate_frames(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )