"""
Oasis RAG Engine — FastAPI Application
Provides endpoints to search the vector database and ingest new documents.
"""

import os
import logging
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

from vector_store import store
import ingestion

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("oasis.rag.api")

app = FastAPI(title="Oasis RAG Engine", version="0.1.0")

# ── Models ───────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    limit: int = 5
    filters: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    id: str | int
    score: float
    text: str
    metadata: Dict[str, Any]

class IngestRequest(BaseModel):
    category: str  # e.g., "health_guidelines", "disaster_protocols"
    source_url: Optional[str] = None

# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    if store.client is None:
        raise HTTPException(status_code=503, detail="Vector store unavailable")
    return {"status": "healthy", "service": "rag-engine"}


@app.post("/search", response_model=List[SearchResult])
async def search(req: SearchRequest):
    """Search for relevant context in the knowledge base."""
    try:
        results = store.search(
            query=req.query,
            limit=req.limit,
            filter_conditions=req.filters
        )
        return results
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Search operation failed")


@app.post("/ingest/local")
async def ingest_local_files(req: IngestRequest, background_tasks: BackgroundTasks):
    """
    Trigger ingestion of local files (markdown/pdf) from the knowledge-base directory.
    Runs asynchronously.
    """
    # Assuming knowledge-base directory is mapped/available via volume or copy
    base_dir = os.environ.get("KNOWLEDGE_BASE_DIR", "/app/knowledge-base")
    target_dir = os.path.join(base_dir, req.category)
    
    if not os.path.exists(target_dir):
        raise HTTPException(status_code=404, detail=f"Category directory not found: {target_dir}")

    background_tasks.add_task(ingestion.process_directory, target_dir, req.category)
    
    return {"message": f"Started ingestion for category '{req.category}' in the background."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
