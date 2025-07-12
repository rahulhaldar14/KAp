from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import requests
import time

app = FastAPI()

PLAYHT_API_KEY = "ak-4c70f443371c4aa8a5ebb7242fae3638"
PLAYHT_USER_ID = "KtkYD7Gbl8O6TPtlcbVqVLWWbRi2"
VOICE_ID = "s3://voice-cloning-zero-shot/ai_female_voice_4/manifest.json"  # You can customize

@app.get("/")
def root():
    return {"message": "Kokoro Play.ht Streaming Server"}

@app.get("/stream")
def stream_voice(text: str = "Hello from Kokoro"):
    # Step 1: Send synthesis request
    payload = {
        "voice": VOICE_ID,
        "content": [text],
        "speed": 1.0
    }
    headers = {
        "Authorization": f"Bearer {PLAYHT_API_KEY}",
        "X-User-Id": PLAYHT_USER_ID,
        "Content-Type": "application/json"
    }

    res = requests.post("https://api.play.ht/api/v2/tts", json=payload, headers=headers)
    if res.status_code != 200:
        return {"error": "TTS request failed", "detail": res.text}

    audio_url = res.json().get("audioUrl")
    if not audio_url:
        return {"error": "Audio URL not returned"}

    # Step 2: Stream audio
    audio_stream = requests.get(audio_url, stream=True)
    return StreamingResponse(audio_stream.iter_content(chunk_size=1024), media_type="audio/mpeg")
