from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTask
from gtts import gTTS
import uuid, os

app = FastAPI(title="TTS API - Giọng Chị Google")

@app.post("/voice/")
async def voice(request: Request):
    data = await request.json()
    text = data.get("text", "")
    
    if not text:
        return {"error": "Chưa có text gửi lên!"}

    # Tạo file mp3 duy nhất
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="vi")
    tts.save(filename)

    # Trả về file và xóa sau khi gửi
    return FileResponse(
        filename,
        media_type="audio/mpeg",
        filename="voice.mp3",
        background=BackgroundTask(lambda: os.remove(filename))
    )
