"""
Oasis Health MCP Server
Provides regional disease outbreak data (e.g., Dengue, Malaria, COVID).
"""

import os
import logging
from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.mcp.health")

app = FastAPI(title="Oasis Health MCP Server", version="0.1.0")

class LocationRequest(BaseModel):
    state: str
    district: str = ""

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "health-mcp"}

@app.post("/mcp/tools/get_disease_data")
async def get_disease_data(req: LocationRequest) -> Dict[str, Any]:
    """MCP Tool: Get active disease outbreaks in a district/state."""
    logger.info(f"Fetching health data for {req.district}, {req.state}")
    
    return {
        "source": "mock_idsp",
        "active_outbreaks": [
            {
                "disease": "Dengue",
                "cases_last_7_days": 142,
                "trend": "increasing",
                "prevention": "Eliminate standing water, use mosquito repellent."
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8014, reload=True)
