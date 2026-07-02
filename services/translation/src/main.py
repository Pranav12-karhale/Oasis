"""
Oasis Translation Service
Integrates with the Bhashini API for Indic language translation.
"""

import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.translation")

app = FastAPI(title="Oasis Translation Service", version="0.1.0")

class TranslationRequest(BaseModel):
    text: str
    source_language: str = "en"
    target_language: str

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "translation"}

@app.post("/translate")
async def translate(req: TranslationRequest):
    """Translate text using Bhashini API."""
    if req.source_language == req.target_language:
        return {"translated_text": req.text}

    logger.info(f"Translating from {req.source_language} to {req.target_language}")
    
    # TODO: Implement real Bhashini API logic here
    # Placeholder implementation
    return {
        "source_language": req.source_language,
        "target_language": req.target_language,
        "original_text": req.text,
        "translated_text": f"[Translated to {req.target_language}]: {req.text}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
