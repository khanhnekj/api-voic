from fastapi import FastAPI, Request
from gtts import gTTS
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.post("/voice/")
async def voice(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text:
        return {"error": "Chưa có text gửi lên!"}

    # Tạo giọng nữ Việt
    tts = gTTS(text=text, lang="vi")  # 'vi' = tiếng Việt nữ Google
    filename = "voice.mp3"
    tts.save(filename)

    return FileResponse(filename, media_type="audio/mpeg", filename="voice.mp3")
