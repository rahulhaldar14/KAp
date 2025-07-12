from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import requests

app = FastAPI()

ELEVENLABS_API_KEY = "sk_5e100d725208770de819733a88cbbd166d01b8835ceeb39a"
VOICE_ID = "asDeXBMC8hUkhqqL7agO"

@app.get("/")
def root():
    return {"message": "Kokoro ElevenLabs Streaming Server"}

@app.get("/stream")
def stream_voice(text: str = "Hello from Kokoro"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)
    if response.status_code != 200:
        return {"error": "TTS request failed", "detail": response.text}

    return StreamingResponse(response.iter_content(chunk_size=1024), media_type="audio/mpeg")
