"""
Oasis Geo/Population MCP Server
Provides population density, demographics, and critical infrastructure locations (hospitals/shelters).
"""

import os
import logging
from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.mcp.geo")

app = FastAPI(title="Oasis Geo MCP Server", version="0.1.0")

class LocationRequest(BaseModel):
    lat: float
    lng: float
    radius_km: float = 5.0

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "geo-mcp"}

@app.post("/mcp/tools/get_infrastructure")
async def get_infrastructure(req: LocationRequest) -> Dict[str, Any]:
    """MCP Tool: Get nearby hospitals and emergency shelters."""
    logger.info(f"Fetching infrastructure near {req.lat}, {req.lng}")
    
    return {
        "source": "mock_osm",
        "hospitals": [
            {"name": "City General Hospital", "distance_km": 1.2, "has_er": True}
        ],
        "shelters": []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8015, reload=True)
