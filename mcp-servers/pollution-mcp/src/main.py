"""
Oasis Pollution MCP Server
Integrates with CPCB (Central Pollution Control Board) and OpenAQ APIs.
"""

import os
import logging
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.mcp.pollution")

app = FastAPI(title="Oasis Pollution MCP Server", version="0.1.0")

class LocationRequest(BaseModel):
    lat: float
    lng: float
    city: str = ""

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "pollution-mcp"}

@app.post("/mcp/tools/get_air_quality")
async def get_air_quality(req: LocationRequest) -> Dict[str, Any]:
    """MCP Tool: Get air quality index and pollutant details."""
    logger.info(f"Fetching AQI for lat:{req.lat} lng:{req.lng} city:{req.city}")
    
    return {
        "source": "mock_cpcb",
        "aqi": 185,
        "category": "Moderate",
        "dominant_pollutant": "PM2.5",
        "pollutants": {
            "pm25": {"value": 85.4, "unit": "µg/m³"},
            "pm10": {"value": 140.2, "unit": "µg/m³"},
            "o3": {"value": 45.1, "unit": "µg/m³"}
        },
        "health_recommendation": "Unusually sensitive people should consider reducing prolonged or heavy exertion."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8011, reload=True)
