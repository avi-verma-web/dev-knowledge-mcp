# Developer Knowledge MCP

A small, deployable MCP server for searching developer documentation and engineering notes.

## Stack
- Python 3.12
- FastAPI + MCP Python SDK (Streamable HTTP transport)
- ChromaDB local persistent vector store for development
- Sentence Transformers embeddings
- Vercel Python functions for the HTTP API

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.index:app --reload
```

## MCP endpoint
When running locally: `http://localhost:8000/mcp`

## Important deployment note
Vercel's serverless filesystem is ephemeral and function execution is bounded. The included local Chroma persistence is for development/testing, not durable production storage. Before using this with persistent user data, connect a hosted vector database and object storage. Keep secrets in environment variables.

## API
- `GET /health` — health check
- `POST /documents` — ingest a text document
- MCP tools: `search_docs`, `list_documents`, `delete_document`
