"""
Oasis Weather MCP Server
Integrates with IMD (India Meteorological Department) and OpenWeatherMap APIs.
"""

import os
import logging
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.mcp.weather")

app = FastAPI(title="Oasis Weather MCP Server", version="0.1.0")

class LocationRequest(BaseModel):
    lat: float
    lng: float
    city: str = ""

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "weather-mcp"}

@app.post("/mcp/tools/get_weather")
async def get_weather(req: LocationRequest) -> Dict[str, Any]:
    """MCP Tool: Get current weather and forecast for a location."""
    # TODO: Implement real IMD / OpenWeatherMap API calls here
    # Mocking for MVP structure
    logger.info(f"Fetching weather for lat:{req.lat} lng:{req.lng} city:{req.city}")
    
    return {
        "source": "mock_imd",
        "current": {
            "temperature": 32.5,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "uv_index": 7,
            "heat_index": 38.2
        },
        "forecast": [
            {"day": "tomorrow", "condition": "Scattered Thunderstorms", "high": 30, "low": 25}
        ],
        "warnings": [
            {"type": "Heat Wave", "severity": "moderate", "message": "Stay hydrated during afternoon hours."}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True)
