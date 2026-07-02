"""
Oasis Disaster MCP Server
Integrates with NDMA SACHET API / RSS feeds for natural disaster alerts.
"""

import os
import logging
from typing import Dict, Any, List

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.mcp.disaster")

app = FastAPI(title="Oasis Disaster MCP Server", version="0.1.0")

class LocationRequest(BaseModel):
    state: str
    district: str = ""

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "disaster-mcp"}

@app.post("/mcp/tools/get_active_alerts")
async def get_active_alerts(req: LocationRequest) -> Dict[str, Any]:
    """MCP Tool: Get active disaster and emergency alerts for a state/district."""
    logger.info(f"Fetching disaster alerts for state:{req.state} district:{req.district}")
    
    return {
        "source": "mock_ndma_sachet",
        "active_alerts": [
            {
                "id": "alert-1234",
                "type": "Flash Flood Warning",
                "severity": "High",
                "certainty": "Observed",
                "urgency": "Immediate",
                "description": "Heavy rainfall has caused flash flooding in low-lying areas. Evacuate to higher ground immediately.",
                "instruction": "Do not attempt to cross flooded roads.",
                "effective": "2026-06-27T10:00:00Z",
                "expires": "2026-06-28T10:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8012, reload=True)
