# SrotGraph Architecture

**Version:** 1.0.0  
**Status:** Draft  
**Last Updated:** 2026-10-15

---

## 1. Architecture Overview

SrotGraph uses a **modular monolith** architecture with the option to extract independent workers for long-running processing tasks. The system is composed of:

1. **Backend API** (FastAPI/Python) — HTTP API, business logic, database access
2. **Frontend** (Next.js/TypeScript) — Web UI for analysts and verifiers
3. **PostgreSQL** — Durable metadata store for streams, claims, evidence, sources, relationships
4. **Redis Streams** — Async job queue for processing tasks
5. **Object Storage** — Local filesystem (initially) for media files and artifacts

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              User Layer                                  │
│  ┌──────────────┐                    ┌──────────────┐                   │
│  │   Web UI     │                    │  API Client  │                   │
│  │  (Next.js)   │                    │   (Future)   │                   │
│  └──────┬───────┘                    └──────┬───────┘                   │
└─────────┼────────────────────────────────────┼───────────────────────────┘
          │ HTTPS                             │ HTTPS
          ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API Layer                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Application                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ Streams  │  │  Claims  │  │ Evidence │  │ Sources  │      │   │
│  │  │ Router   │  │  Router  │  │  Router  │  │  Router  │      │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │  Jobs    │  │ Metrics  │  │  Health  │  │  Config  │      │   │
│  │  │ Router   │  │ Router   │  │  Check   │  │  Settings│      │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                          │              │                                │
│              ┌───────────┘              └───────────┐                  │
│              ▼                                       ▼                  │
│  ┌─────────────────────┐               ┌─────────────────────┐         │
│  │   SQLAlchemy ORM    │               │   AI Provider       │         │
│  │   (PostgreSQL)      │               │   Interface         │         │
│  └─────────────────────┘               └─────────┬───────────┘         │
│                                                  │                       │
└──────────────────────────────────────────────────┼───────────────────────┘
                                                   │
                    ┌──────────────────────────────┼──────────────────────┐
                    │                              │                      │
                    ▼                              ▼                      │
┌─────────────────────────┐        ┌──────────────────────────────────┐ │
│   Redis Streams         │        │      AI Provider Implementations │ │
│   (Job Queue)           │        │  ┌─────────┐ ┌─────────┐        │ │
│                         │        │  │  Mock   │ │ Whisper │        │ │
│  ┌───────────────────┐  │        │  │Provider │ │Provider │        │ │
│  │ Processing Jobs   │  │        │  └─────────┘ └─────────┘        │ │
│  │ Claim Extraction  │  │        │  ┌─────────┐ ┌─────────┐        │ │
│  │ Evidence Analysis │  │        │  │  OpenAI │ │DeepGram │        │ │
│  └───────────────────┘  │        │  │Provider │ │Provider │        │ │
│                         │        │  └─────────┘ └─────────┘        │ │
└─────────────────────────┘        └──────────────────────────────────┘ │
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Data Layer                                      │
│  ┌─────────────────────┐              ┌─────────────────────┐          │
│  │    PostgreSQL       │              │   Object Storage    │          │
│  │                     │              │   (Local FS/ S3)    │          │
│  │  - streams          │              │                     │          │
│  │  - claims           │              │  - audio files      │          │
│  │  - claim_versions   │              │  - video files      │          │
│  │  - evidence         │              │  - transcripts      │          │
│  │  - sources          │              │  - snapshots        │          │
│  │  - relationships    │              │  - artifacts        │          │
│  │  - jobs             │              │                     │          │
│  │  - metrics          │              │                     │          │
│  └─────────────────────┘              └─────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Responsibilities

### 2.1 FastAPI Backend

**Location:** `backend/srotgraph/`

| Component | Responsibility |
|-----------|----------------|
| `main.py` | Application factory, middleware, health endpoints |
| `config.py` | Pydantic settings from environment variables |
| `routes/` | API endpoint handlers (streams, claims, evidence, etc.) |
| `models/` | SQLAlchemy ORM models |
| `schemas/` | Pydantic schemas for request/response validation |
| `services/` | Business logic layer |
| `providers/` | AI provider interface and implementations |
| `workers/` | Async job processors (can run standalone) |
| `db/` | Database connection, session management, migrations |

### 2.2 Frontend (Next.js)

**Location:** `frontend/src/`

| Component | Responsibility |
|-----------|----------------|
| `app/` | Next.js App Router pages (dashboard, stream detail, claim review) |
| `components/` | React components (claim cards, evidence panels, metric charts) |
| `lib/api.ts` | Typed API client for backend communication |
| `types/index.ts` | TypeScript type definitions matching backend schemas |
| `lib/` | Utility functions, state management (future) |

### 2.3 AI Providers

**Location:** `backend/srotgraph/providers/`

Providers are interchangeable implementations behind a common interface:

```
┌─────────────────────────────────────────────────────────────┐
│                    Provider Interface                        │
├─────────────────────────────────────────────────────────────┤
│  SpeechRecognizer (ABC)                                     │
│  ├── transcribe(audio_path) -> Transcript                   │
│  └── supported_formats() -> list[str]                      │
│                                                             │
│  ClaimExtractor (ABC)                                      │
│  ├── extract_claims(text, context) -> list[ClaimProposal]  │
│  └── extract_relationships(claims) -> list[RelProposal]    │
│                                                             │
│  EvidenceAnalyzer (ABC)                                    │
│  ├── analyze(evidence) -> AnalysisResult                    │
│  └── verify(claim, evidence) -> VerificationResult         │
└─────────────────────────────────────────────────────────────┘
```

| Provider | Type | Status |
|----------|------|--------|
| `MockSpeechRecognizer` | Speech-to-text | Implemented (returns deterministic data) |
| `MockClaimExtractor` | Claim extraction | Implemented (returns deterministic data) |
| `WhisperProvider` | Speech-to-text | Planned (OpenAI Whisper local) |
| `DeepGramProvider` | Speech-to-text | Planned (cloud API) |
| `AssemblyAIProvider` | Speech-to-text | Planned (cloud API) |
| `OpenAIClaimExtractor` | Claim extraction | Planned (GPT models) |
| `AnthropicClaimExtractor` | Claim extraction | Planned (Claude models) |
| `GoogleClaimExtractor` | Claim extraction | Planned (Gemini models) |

### 2.4 Database (PostgreSQL)

Stores all metadata. Uses SQLAlchemy with asyncpg driver.

**Key design principles:**
- All tables have `created_at` and `updated_at` timestamps
- Claims and relationships preserve history (claim_versions table)
- Soft deletes where appropriate (deleted_at column)
- Indexes on foreign keys and frequently queried columns
- JSONB for flexible metadata storage

### 2.5 Redis Streams

Used for async job processing:

```
Stream: srotgraph:jobs
  ├── job:{id} — Job payload and status
  ├── job:{id}:progress — Progress updates
  └── job:{id}:result — Final result or error
```

Workers consume from streams and process jobs idempotently.

### 2.6 Object Storage

Initially local filesystem under `backend/storage/`. Future: S3-compatible storage.

```
storage/
├── audio/
│   └── {stream_id}.mp3
├── video/
│   └── {stream_id}.mp4
├── transcripts/
│   └── {stream_id}.json
├── snapshots/
│   └── {stream_id}/{timestamp}.png
└── artifacts/
    └── {job_id}/
```

---

## 3. Data Flow

### 3.1 Stream Ingestion Flow

```
User uploads file
       │
       ▼
┌──────────────────┐
│  API: POST       │
│  /streams        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Validate input  │
│  Save to DB      │
│  (status=pending)│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Queue job       │
│  (transcription) │───────────┐
└────────┬─────────┘           │
         │                     │
         ▼                     ▼
┌──────────────────┐   ┌──────────────────┐
│  Return job ID   │   │  Worker picks up │
│  to client       │   │  job from queue  │
└──────────────────┘   └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Download/access  │
                        │  media file       │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Call provider   │
                        │  (speech rec)     │
                        └────────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
            ┌──────────────┐          ┌──────────────┐
            │   Success    │          │   Failure    │
            │  Save trans- │          │  Retry /     │
            │  script to   │          │  Mark failed │
            │  storage     │          └──────────────┘
            └──────┬───────┘
                   │
                   ▼
            ┌──────────────────┐
            │  Queue claim     │
            │  extraction job  │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │  Worker extracts │
            │  claims from     │
            │  transcript       │
            └────────┬─────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
   ┌────────────┐         ┌────────────┐
   │  Success   │         │  Failure   │
   │  Save      │         │  Retry     │
   │  claims to │         │  / Mark    │
   │  DB        │         │  failed    │
   └─────┬──────┘         └────────────┘
         │
         ▼
   ┌──────────────────┐
   │  Update stream   │
   │  status to       │
   │  completed       │
   └──────────────────┘
```

### 3.2 Claim Review Flow

```
User opens claim detail
         │
         ▼
┌──────────────────┐
│  GET /claims/{id}│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Load claim from │
│  PostgreSQL       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Load claim      │
│  versions        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Load evidence   │
│  for claim       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Load             │
│  relationships   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Render UI with  │
│  claim, versions,│
│  evidence, rels  │
└──────────────────┘
```

### 3.3 Claim Validation Flow

```
User validates claim
         │
         ▼
┌──────────────────┐
│  PATCH           │
│  /claims/{id}/  │
│  status          │
│  {status:        │
│   "validated"}   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Update claim    │
│  status in DB    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Log validation  │
│  event           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Update metrics  │
│  (claims_validated│
│   incremented)   │
└──────────────────┘
```

---

## 4. Public API Boundaries

### 4.1 REST API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/` | API info |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |
| `GET` | `/openapi.json` | OpenAPI schema |
| `POST` | `/api/v1/streams` | Create stream |
| `GET` | `/api/v1/streams` | List streams |
| `GET` | `/api/v1/streams/{id}` | Get stream |
| `DELETE` | `/api/v1/streams/{id}` | Delete stream |
| `POST` | `/api/v1/claims` | Create claim |
| `GET` | `/api/v1/claims` | List claims |
| `GET` | `/api/v1/claims/{id}` | Get claim |
| `PATCH` | `/api/v1/claims/{id}/status` | Update claim status |
| `GET` | `/api/v1/claims/{id}/evolution` | Get claim evolution |
| `POST` | `/api/v1/evidence` | Create evidence |
| `GET` | `/api/v1/evidence` | List evidence |
| `GET` | `/api/v1/evidence/{id}` | Get evidence |
| `PATCH` | `/api/v1/evidence/{id}/verify` | Verify evidence |
| `POST` | `/api/v1/sources` | Create source |
| `GET` | `/api/v1/sources` | List sources |
| `GET` | `/api/v1/sources/{id}` | Get source |
| `POST` | `/api/v1/relationships` | Create relationship |
| `GET` | `/api/v1/relationships` | List relationships |
| `GET` | `/api/v1/relationships/{id}` | Get relationship |
| `PATCH` | `/api/v1/relationships/{id}/status` | Update relationship status |
| `GET` | `/api/v1/jobs/{id}` | Get job status |
| `GET` | `/api/v1/jobs` | List jobs |
| `GET` | `/api/v1/metrics/processing` | Processing metrics |
| `GET` | `/api/v1/metrics/accuracy` | Accuracy metrics |
| `GET` | `/api/v1/metrics/performance` | Performance metrics |

### 4.2 API Design Principles

1. **Resource-oriented URLs** — nouns, not verbs
2. **Standard HTTP methods** — GET (read), POST (create), PATCH (update), DELETE (remove)
3. **JSON request/response bodies**
4. **Pagination** for list endpoints (`page`, `page_size`, `has_more`)
5. **Consistent error format** — `{"detail": "error message"}`
6. **Idempotent operations where possible**
7. **Versioned via URL prefix** (`/api/v1/`)

### 4.3 Authentication (Future)

Not implemented in initial version. When added:
- API key authentication for programmatic access
- Session-based auth for web UI
- Role-based access control (analyst, verifier, admin)

---

## 5. Security Requirements

### 5.1 Credential Management

- All API keys (OpenAI, Anthropic, DeepGram, AssemblyAI) supplied via environment variables
- Never logged or exposed in API responses
- `.env` files excluded from version control (`.gitignore`)

### 5.2 Data Protection

- No private media content in logs
- Error messages should not leak internal details
- File uploads validated for type and size

### 5.3 Future Considerations

- HTTPS in production (handled by reverse proxy or platform)
- Rate limiting on API endpoints
- Authentication and authorization
- Input validation and sanitization

---

## 6. Testing Strategy

### 6.1 Test Pyramid

```
        ┌─────────┐
       / ┌───────┐ ┘
      /  │  E2E  │  ┌─────────┐
     /   └───────┘ / │   Uses  │
    /    ┌───────┐ ┘  │  Real    │
   /     │ Int.  │────│ Integr.  │
   │     └───────┘    │  Test    │
┌──┴───┐   ┌───────┐ └─────────┘
│ Unit │───│  API  │
│ Tests│   │Tests  │
└──────┘   └───────┘
   │           │
   ▼           ▼
 Many        Fewer
 Fast        Slower
```

### 6.2 Unit Tests

- Test individual functions and classes in isolation
- Mock external dependencies (database, APIs)
- Run fast, no external services needed
- Coverage target: core business logic

### 6.3 Integration Tests

- Test API endpoints with test database
- Use testcontainers or separate test database
- Test provider interfaces with mock implementations
- Verify request/response schemas

### 6.4 End-to-End Tests

- Test complete workflows via frontend or API
- Use Docker Compose with real PostgreSQL and Redis
- Test critical user journeys

### 6.5 Mock Providers

- `MockSpeechRecognizer` returns deterministic transcript data
- `MockClaimExtractor` returns deterministic claims
- Allows testing without paid API access
- Can simulate success, failure, and edge cases

---

## 7. Scalability Considerations

### 7.1 Horizontal Scaling

- FastAPI app is stateless — can scale horizontally behind load balancer
- PostgreSQL can scale with read replicas (future)
- Redis Streams supports multiple consumers

### 7.2 Async Processing

- Long-running tasks (transcription, claim extraction) are offloaded to workers
- Workers can scale independently based on queue depth
- Each job is processed by one worker at a time (idempotency via Redis)

### 7.3 Storage

- Object storage can migrate from local filesystem to S3-compatible storage
- Database can be migrated to managed PostgreSQL (RDS, Supabase, etc.)

---

## 8. Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend language | Python 3.12+ | Mature ecosystem for AI/ML, FastAPI for APIs |
| API framework | FastAPI | Async support, automatic OpenAPI docs, Pydantic validation |
| Database | PostgreSQL | Relational, ACID, mature, good JSONB support |
| ORM | SQLAlchemy 2.0 | Async support, mature, flexible |
| Job queue | Redis Streams | Simple, well-understood, supports consumer groups |
| Frontend framework | Next.js 14+ | React, App Router, TypeScript, good ecosystem |
| Styling | Tailwind CSS | Utility-first, consistent design, small bundle |
| Containerization | Docker + Compose | Local development, deployment consistency |
| Speech recognition | Pluggable | Support local (Whisper) and cloud (DeepGram, AssemblyAI) |
| Claim extraction | Pluggable | Support OpenAI, Anthropic, Google |

---

## 9. Assumptions and Constraints

1. **Single-region deployment initially** — no multi-region replication
2. **Moderate throughput initially** — thousands of streams per day, not millions
3. **Files are not extremely large** — videos under a few hours, audio files reasonable size
4. **AI provider APIs are reliable enough** — with retry logic for transient failures
5. **PostgreSQL can handle the metadata load** — claims are text, not massive data

---

## 10. Future Architecture Evolution

Potential future changes:
- Extract workers into separate services if scale demands it
- Add dedicated search service (Elasticsearch, pgvector)
- Add caching layer (Redis for API responses)
- Add message broker (RabbitMQ, Kafka) if Redis Streams becomes limiting
- Add graph database for relationship queries if complexity grows

---

*This architecture will evolve as the project progresses. Significant changes should be captured in architecture decision records in `docs/decisions/`.*
