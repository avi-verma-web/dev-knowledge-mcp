from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from typing import Any

import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from mcp.server.fastmcp import FastMCP

DATA_DIR = os.getenv("CHROMA_PATH", "/tmp/dev-knowledge-chroma")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "developer_knowledge")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

mcp = FastMCP("developer-knowledge", stateless_http=True, json_response=True)
client: chromadb.ClientAPI | None = None
collection: chromadb.Collection | None = None
embedder: SentenceTransformer | None = None


def resources() -> tuple[chromadb.Collection, SentenceTransformer]:
    global client, collection, embedder
    if collection is None:
        os.makedirs(DATA_DIR, exist_ok=True)
        client = chromadb.PersistentClient(path=DATA_DIR)
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    if embedder is None:
        embedder = SentenceTransformer(EMBEDDING_MODEL)
    return collection, embedder


@mcp.tool()
def search_docs(query: str, limit: int = 5) -> dict[str, Any]:
    """Find the most relevant stored developer documents for a natural-language query."""
    if not query.strip():
        raise ValueError("query must not be empty")
    limit = max(1, min(limit, 20))
    docs, model = resources()
    result = docs.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=min(limit, max(1, docs.count())),
        include=["documents", "metadatas", "distances"],
    )
    items = []
    for i, doc in enumerate(result.get("documents", [[]])[0]):
        items.append({
            "content": doc,
            "metadata": (result.get("metadatas") or [[]])[0][i],
            "distance": (result.get("distances") or [[]])[0][i],
        })
    return {"query": query, "results": items}


@mcp.tool()
def list_documents(limit: int = 50) -> dict[str, Any]:
    """List stored document IDs and metadata."""
    docs, _ = resources()
    result = docs.get(limit=max(1, min(limit, 200)), include=["metadatas"])
    return {
        "documents": [
            {"id": doc_id, "metadata": (result.get("metadatas") or [None] * len(result["ids"]))[i]}
            for i, doc_id in enumerate(result["ids"])
        ]
    }


@mcp.tool()
def delete_document(document_id: str) -> dict[str, str]:
    """Delete a document by its ID."""
    docs, _ = resources()
    docs.delete(ids=[document_id])
    return {"deleted": document_id}


class DocumentInput(BaseModel):
    text: str = Field(min_length=1, max_length=100_000)
    source: str = Field(default="manual", max_length=500)
    metadata: dict[str, Any] = Field(default_factory=dict)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(title="Developer Knowledge MCP", version="0.1.0", lifespan=lifespan)
app.mount("/mcp", mcp.streamable_http_app())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "developer-knowledge-mcp"}


@app.post("/documents")
def ingest_document(payload: DocumentInput) -> dict[str, str]:
    try:
        docs, model = resources()
        document_id = str(uuid.uuid4())
        metadata = {"source": payload.source, **payload.metadata}
        docs.add(
            ids=[document_id],
            documents=[payload.text],
            metadatas=[metadata],
            embeddings=[model.encode(payload.text).tolist()],
        )
        return {"id": document_id, "status": "indexed"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Document ingestion failed") from exc
