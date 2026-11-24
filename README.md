# Avinash Verma Portfolio MCP

A public, read-only MCP server that lets ChatGPT and other MCP-compatible assistants retrieve professional information from Avinash Verma's portfolio.

## Tools
- `get_profile` — professional summary and public links
- `get_skills` — portfolio-listed technical skills
- `get_projects` — project descriptions, demos and repositories
- `search_portfolio` — keyword search across the public portfolio data

## Endpoints
- `/mcp` — MCP Streamable HTTP endpoint
- `/health` — health check
- `/privacy` — privacy policy
- `/terms` — terms of use

## Source
Portfolio: https://avinash-verma.netlify.app/
Portfolio source repository: https://github.com/avi-verma-web/avi-portfolio-parcel

## Local development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.index:app --reload
```

The server is read-only. It does not use embeddings, a vector database, authentication, or persistent user storage.
