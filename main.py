from fastapi import FastAPI, Request
from gtts import gTTS
from fastapi.responses import FileResponse
import os
import uuid

app = FastAPI(title="TTS API - Giọng Chị Google")

@app.post("/voice/")
async def voice(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text:
        return {"error": "Chưa có text gửi lên!"}

    # Tạo file tạm với tên duy nhất
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="vi")
    tts.save(filename)

    # Trả về file và xóa sau khi gửi
    response = FileResponse(filename, media_type="audio/mpeg", filename="voice.mp3")
    # Dùng background task để xóa file sau khi gửi
    from fastapi.background import BackgroundTask
    response.background = BackgroundTask(lambda: os.remove(filename))
    return response
