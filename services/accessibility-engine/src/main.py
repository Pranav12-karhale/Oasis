"""
Oasis Accessibility Engine
Centralized service for generating ARIA labels, visual alerts, and ISL mapping.
"""

import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel

from aria_generator import generate_aria
from visual_alerts import map_severity_to_visuals
from isl_processor import simplify_for_isl

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.accessibility")

app = FastAPI(title="Oasis Accessibility Engine", version="0.1.0")

class AdvisoryRequest(BaseModel):
    text: str
    severity: str
    context_type: str = "health"

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "accessibility"}

@app.post("/process")
async def process_advisory(req: AdvisoryRequest):
    """Process an advisory for various accessibility modes."""
    
    # 1. Generate ARIA context for blind users
    aria_context = generate_aria(req.text, req.severity, req.context_type)
    
    # 2. Map to visual alerts (colors, icons, vibrations) for deaf/hard-of-hearing
    visual_context = map_severity_to_visuals(req.severity, req.context_type)
    
    # 3. Simplify text for ISL mode / cognitive accessibility
    simplified_text = simplify_for_isl(req.text)
    
    return {
        "original_text": req.text,
        "aria": aria_context,
        "visuals": visual_context,
        "simplified_text": simplified_text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)
