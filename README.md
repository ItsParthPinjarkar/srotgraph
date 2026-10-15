# SrotGraph

**Evidence-Preserving Intelligence System**

SrotGraph processes continuous or recorded audio, video and text streams, extracts timestamped claims, tracks claim evolution, connects evidence and sources, and measures accuracy, latency, memory consumption and information loss.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SrotGraph System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Streams    │───▶│  AI Providers │───▶│   Claims     │      │
│  │  (Audio/     │    │ (Whisper,    │    │  (Timestamped │      │
│  │   Video/     │    │  DeepGram,   │    │   Assertions) │      │
│  │   Text)      │    │  AssemblyAI) │    │              │      │
│  └──────────────┘    └──────────────┘    └──────┬───────┘      │
│                                                  │              │
│  ┌──────────────┐    ┌──────────────┐           │              │
│  │   Metrics    │◀───│  Validation  │◀──────────┘              │
│  │ (Accuracy/   │    │   Engine     │                         │
│  │  Latency/    │    └──────────────┘                         │
│  │  Memory)     │                                            │
│  └──────────────┘                                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Data Layer                                     ││
│  │  PostgreSQL (Claims, Evidence, Sources, History)           ││
│  │  Redis Streams (Async Job Processing)                      ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
srotgraph/
├── AGENTS.md              # Coding agent rules and guidelines
├── README.md             # This file
├── docker-compose.yml    # Full stack deployment
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── .env.example
│   ├── README.md
│   ├── srotgraph/
│   │   ├── __init__.py
│   │   ├── config.py      # Application settings
│   │   └── main.py        # FastAPI application entry point
│   └── tests/
│       ├── __init__.py
│       └── test_main.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── pnpm-lock.yaml
    ├── .env.local
    ├── README.md
    ├── next.config.ts
    ├── src/
    │   ├── app/          # Next.js App Router pages
    │   ├── components/   # React components
    │   ├── lib/
    │   │   └── api.ts    # API client
    │   └── types/
    │       └── index.ts  # TypeScript type definitions
    └── ...
```

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- pnpm
- Docker and Docker Compose (optional, for containerized setup)
- PostgreSQL (optional, for local development)
- Redis (optional, for async processing)

### Development Setup

#### 1. Clone and Install

```bash
# Backend
cd backend
pip install -e ".[dev]"

# Frontend
cd frontend
pnpm install
```

#### 2. Configure Environment

Copy `.env.example` to `.env` in the backend directory and adjust as needed:

```bash
cd backend
cp .env.example .env
```

#### 3. Run the Services

```bash
# Terminal 1: Backend API
cd backend
uvicorn srotgraph.main:app --reload

# Terminal 2: Frontend
cd frontend
pnpm dev
```

#### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Docker Setup

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## API Overview

### Endpoints

| Category | Endpoints | Description |
|----------|-----------|-------------|
| Health | `GET /health`, `GET /` | Health checks and API info |
| Streams | `/api/v1/streams` | Audio/video/text stream management |
| Claims | `/api/v1/claims` | Timestamped claim extraction and tracking |
| Evidence | `/api/v1/evidence` | Evidence collection and verification |
| Sources | `/api/v1/sources` | Source management and reliability scoring |
| Relationships | `/api/v1/relationships` | Claim relationships and connections |
| Jobs | `/api/v1/jobs` | Async processing job status |
| Metrics | `/api/v1/metrics/*` | Processing, accuracy, and performance metrics |

### Type-Safe API Client

The frontend includes a fully typed API client at `src/lib/api.ts` with all endpoints defined. See `src/types/index.ts` for the complete type definitions.

## AI Provider Configuration

SrotGraph supports interchangeable AI providers through environment variables:

### Speech Recognition
- `mock` — Deterministic mock provider (default, no API key needed)
- `whisper` — OpenAI Whisper
- `deepgram` — DeepGram API
- `assemblyai` — AssemblyAI API

### Claim Extraction
- `mock` — Deterministic mock provider (default)
- `openai` — OpenAI GPT models
- `anthropic` — Anthropic Claude models
- `google` — Google Gemini models

### Retrieval
- `mock` — In-memory mock retrieval (default)
- `pgvector` — PostgreSQL vector search
- `external` — External vector database

Set the provider and API key via environment variables:

```bash
# .env
SPEECH_RECOGNITION_PROVIDER=deepgram
DEEPGRAM_API_KEY=your_api_key_here

CLAIM_EXTRACTION_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

## Development Guidelines

See [AGENTS.md](AGENTS.md) for the complete coding agent rules:

1. Work on one milestone at a time
2. Define typed interfaces before integrating components
3. Use mock providers for testing, never require paid APIs for tests
4. Preserve timestamps, provenance, and historical claim versions
5. Treat AI-generated claims as uncertain proposals until validated
6. Write automated tests for all new functionality

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Type Checking

```bash
cd frontend
npx tsc --noEmit
```

### Frontend linting

```bash
cd frontend
pnpm lint
```

## License

This project is open source. See the LICENSE file for details.
