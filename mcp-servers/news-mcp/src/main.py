"""
Oasis News/Conflict MCP Server
Aggregates news, local conflict reports, and social unrest indicators.
"""

import os
import logging
from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.mcp.news")

app = FastAPI(title="Oasis News/Conflict MCP Server", version="0.1.0")

class LocationRequest(BaseModel):
    state: str
    city: str = ""

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "news-mcp"}

@app.post("/mcp/tools/get_local_news")
async def get_local_news(req: LocationRequest) -> Dict[str, Any]:
    """MCP Tool: Get active news and conflict/unrest reports for an area."""
    logger.info(f"Fetching news for {req.city}, {req.state}")
    
    return {
        "source": "mock_news_aggregator",
        "conflict_level": "Low",
        "recent_reports": [
            {"headline": "Local elections concluding peacefully", "sentiment": "positive"},
            {"headline": "Traffic diversions due to marathon", "sentiment": "neutral", "impacts_travel": True}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8013, reload=True)
