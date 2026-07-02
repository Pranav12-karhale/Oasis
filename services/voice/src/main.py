"""
Oasis Voice Service
Handles Automatic Speech Recognition (ASR) and Text-to-Speech (TTS) via Bhashini API.
"""

import os
import logging
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel

from tts_engine import synthesize_audio
from conversation_manager import ConversationManager
from voice_navigator import process_voice_command

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.voice")

app = FastAPI(title="Oasis Voice Service", version="0.1.0")
conv_manager = ConversationManager()

class TTSRequest(BaseModel):
    text: str
    language: str
    voice_gender: str = "female"
    speed: float = 1.0

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "voice"}

@app.post("/asr")
async def speech_to_text(audio: UploadFile = File(...), language: str = Form("auto")):
    """Convert uploaded audio file to text."""
    logger.info(f"Received audio file for ASR, target language: {language}")
    
    # TODO: Implement Bhashini ASR
    # MOCK RESPONSE
    return {
        "text": "What is the air quality today?",
        "detected_language": "en"
    }

@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    """Convert text to speech audio URL/bytes."""
    logger.info(f"Synthesizing TTS for {req.language}")
    audio_url = synthesize_audio(req.text, req.language, req.voice_gender, req.speed)
    return {"audio_url": audio_url}

@app.post("/command")
async def handle_voice_command(text: str):
    """Process app navigation / action commands (e.g., 'Go to alerts')."""
    return process_voice_command(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
