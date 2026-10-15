# SrotGraph Backend

FastAPI backend for the SrotGraph evidence-preserving intelligence system.

## Architecture

The backend provides:
- REST API for stream processing and claim extraction
- PostgreSQL for persistent storage of claims, evidence, and sources
- Redis Streams for asynchronous job processing
- Pluggable AI provider interfaces for speech recognition, claim extraction, and retrieval

## Setup

```bash
cd backend
pip install -e ".[dev]"
```

## Environment variables

See `.env.example` for required configuration.

## Running

```bash
uvicorn srotgraph.main:app --reload
```

## Testing

```bash
pytest
```
