"""
Oasis RAG Engine — Vector Store Manager
Handles connections to Qdrant, document embeddings, and hybrid search.
"""

import os
import logging
from typing import List, Dict, Any, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, ScoredPoint
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("oasis.rag.store")

# ── Configuration ────────────────────────────────────────────────────────────
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_PREFIX", "oasis") + "_knowledge"

# Load embedding model locally (zero-cost)
# all-MiniLM-L6-v2 is lightweight and fast for CPU inference
MODEL_NAME = "all-MiniLM-L6-v2"
logger.info(f"Loading embedding model: {MODEL_NAME}")
embedding_model = SentenceTransformer(MODEL_NAME)
VECTOR_SIZE = embedding_model.get_sentence_embedding_dimension()


class VectorStore:
    def __init__(self):
        """Initialize connection to Qdrant."""
        try:
            self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            self._ensure_collection()
            logger.info(f"Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self.client = None

    def _ensure_collection(self):
        """Ensure the target collection exists in Qdrant, create if not."""
        if not self.client:
            return

        collections = self.client.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)

        if not exists:
            logger.info(f"Creating new collection: {COLLECTION_NAME}")
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
        else:
            logger.info(f"Collection {COLLECTION_NAME} already exists.")

    def embed_text(self, text: str) -> List[float]:
        """Convert text to vector embedding."""
        # Returns a numpy array, convert to list of floats for Qdrant
        return embedding_model.encode(text).tolist()

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Embed and insert documents into Qdrant.
        Expected format: [{"id": "uuid", "text": "content", "metadata": {...}}]
        """
        if not self.client:
            raise ConnectionError("Qdrant client not initialized")

        points = []
        for doc in documents:
            vector = self.embed_text(doc["text"])
            points.append(
                PointStruct(
                    id=doc["id"],
                    vector=vector,
                    payload={
                        "text": doc["text"],
                        **doc.get("metadata", {})
                    }
                )
            )

        if points:
            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            logger.info(f"Inserted {len(points)} documents into Qdrant.")

    def search(
        self, 
        query: str, 
        limit: int = 5, 
        filter_conditions: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using dense vector similarity.
        """
        if not self.client:
            raise ConnectionError("Qdrant client not initialized")

        query_vector = self.embed_text(query)
        
        # TODO: Implement proper Qdrant Filter logic based on filter_conditions
        qdrant_filter = None 

        search_result: List[ScoredPoint] = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=limit
        )

        results = []
        for point in search_result:
            results.append({
                "id": point.id,
                "score": point.score,
                "text": point.payload.get("text", ""),
                "metadata": {k: v for k, v in point.payload.items() if k != "text"}
            })

        return results

# Singleton instance
store = VectorStore()
