# ADR 0001: Modular Monolith Architecture with Pluggable Workers

**Status:** Accepted  
**Date:** 2026-10-15  
**Deciders:** Parth Patel (project lead)

---

## 1. Context

SrotGraph needs an architecture that can:
- Process audio, video, and text streams through multiple stages
- Extract timestamped claims using AI providers
- Track claim evolution and evidence connections
- Scale from development (single machine) to production (multiple workers)

We considered several architectural approaches:
1. **Microservices** — Each component as a separate service
2. **Modular monolith** — Single codebase, modular internal structure
3. **Serverless functions** — Event-driven, scale-to-zero
4. **Traditional monolith** — Single application, less internal structure

---

## 2. Decision

We will use a **modular monolith** architecture with the following characteristics:

### 2.1 Core Principles

1. **Single deployable unit** — The FastAPI application is the primary deployable
2. **Internal modularity** — Clear separation between routes, services, providers, and workers
3. **Pluggable AI providers** — All AI integrations behind interfaces, swappable via config
4. **Async job processing** — Long-running tasks offloaded to workers consuming from Redis Streams
5. **Workers can run standalone** — Processing workers are separate entry points that can be scaled independently

### 2.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Modular Monolith                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   FastAPI App                        │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │   │
│  │  │  Routes  │ │ Services │ │  Models  │           │   │
│  │  │          │ │          │ │          │           │   │
│  │  │  streams │ │ stream_  │ │  Stream  │           │   │
│  │  │  claims  │ │ service  │ │  Claim   │           │   │
│  │  │  evidence│ │ claim_   │ │  Evidence│           │   │
│  │  │  sources │ │ service  │ │  Source  │           │   │
│  │  │  jobs    │ │ evidence_│ │  Job     │           │   │
│  │  │  metrics │ │ service  │ │  Metric  │           │   │
│  │  └──────────┘ └──────────┘ └──────────┘           │   │
│  │                           │                         │   │
│  │  ┌─────────────────────────┴───────────────────┐  │   │
│  │  │              Provider Interfaces              │  │   │
│  │  │  SpeechRecognizer │ ClaimExtractor │ ...     │  │   │
│  │  └───────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                 │
│          ┌─────────────────┴─────────────────┐             │
│          ▼                                   ▼             │
│  ┌─────────────────┐               ┌─────────────────┐    │
│  │  PostgreSQL     │               │  Redis Streams  │    │
│  │  (metadata)     │               │  (job queue)    │    │
│  └─────────────────┘               └─────────────────┘    │
│                            │                                 │
│          ┌─────────────────┴─────────────────┐             │
│          ▼                                   ▼             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Standalone Workers (optional)          │  │
│  │  ┌──────────────┐  ┌──────────────┐                │  │
│  │  │ Transcription │  │ Claim        │                │  │
│  │  │ Worker        │  │ Extraction   │                │  │
│  │  │               │  │ Worker       │                │  │
│  │  └──────────────┘  └──────────────┘                │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Module Structure

```
backend/srotgraph/
├── main.py              # Application factory, entry point
├── config.py            # Configuration from environment
├── db/                  # Database setup, session management
│   ├── base.py          # Declarative base
│   ├── session.py       # Async session factory
│   └── migrations/      # Alembic migrations
├── models/              # SQLAlchemy ORM models
│   ├── stream.py
│   ├── claim.py
│   ├── evidence.py
│   ├── source.py
│   ├── relationship.py
│   └── job.py
├── schemas/             # Pydantic schemas for validation
│   ├── stream.py
│   ├── claim.py
│   └── ...
├── routes/              # FastAPI route handlers
│   ├── streams.py
│   ├── claims.py
│   ├── evidence.py
│   ├── sources.py
│   ├── relationships.py
│   ├── jobs.py
│   └── metrics.py
├── services/            # Business logic
│   ├── stream_service.py
│   ├── claim_service.py
│   ├── evidence_service.py
│   └── ...
├── providers/           # AI provider interface + implementations
│   ├── base.py          # Abstract base classes
│   ├── mock/            # Mock implementations
│   │   ├── speech.py
│   │   └── claims.py
│   ├── whisper/         # Whisper provider (future)
│   ├── deepgram/        # DeepGram provider (future)
│   └── openai/          # OpenAI provider (future)
├── workers/             # Async job processors
│   ├── base.py          # Worker base class
│   ├── transcription.py
│   └── claim_extraction.py
└── storage/             # Object storage abstraction
    ├── base.py
    └── local.py         # Local filesystem implementation
```

### 2.4 Worker Design

Workers are designed to be optionally separate processes:

```python
# workers/transcription.py
async def process_transcription_job(job_id: str, stream_id: str):
    """Process a single transcription job."""
    # 1. Get stream and media path from database
    # 2. Call speech recognition provider
    # 3. Save transcript to storage
    # 4. Update job status in database
    # 5. Queue claim extraction job if successful
```

Workers can run as:
- Part of the main FastAPI process (for development/single-machine)
- Separate processes (for production/scaling)

---

## 3. Consequences

### 3.1 Positive

- **Simple deployment** — One main service to deploy
- **Easy development** — All code in one place, easy to navigate
- **Clear boundaries** — Internal modules have defined responsibilities
- **Scalable when needed** — Workers can be extracted and scaled independently
- **Provider agnostic** — AI providers are interchangeable without code changes

### 3.2 Negative

- **Single point of scaling** — The main app scales as a unit (can be addressed with multiple replicas behind LB)
- **Potential for module coupling** — Requires discipline to maintain boundaries
- **Deployment unit is larger** — Changes to any module require full redeployment

### 3.3 Mitigations

- Workers consuming from Redis Streams can be horizontally scaled independently
- Internal APIs between modules are defined through service interfaces
- Database access is isolated to the data layer

---

## 4. Alternatives Considered

### 4.1 Microservices

**Pros:**
- Independent scaling of each component
- Technology diversity (different languages for different services)
- Independent deployment

**Cons:**
- Significant operational complexity
- Network calls between services
- Distributed transaction management
- Overhead for a project of this scale

**Why rejected:** Premature optimization for scale. The operational burden outweighs benefits at current scale expectations.

### 4.2 Serverless Functions

**Pros:**
- Scale to zero
- Pay for actual usage
- No server management

**Cons:**
- Cold start latency
- Limited execution time
- Vendor lock-in
- Debugging complexity
- Not all tasks fit the model (long-running transcription)

**Why rejected:** Too restrictive for long-running media processing. Better fit for event-driven microservices than our batch-oriented processing.

### 4.3 Traditional Monolith (No Internal Modularity)

**Pros:**
- Simplest possible structure
- Minimal overhead

**Cons:**
- Harder to maintain boundaries as project grows
- Harder to extract components later if needed
- Provider interfaces less clear

**Why rejected:** The modular approach adds minimal complexity while providing significant benefits for maintainability and future evolution.

---

## 5. Compliance with Project Rules

This decision aligns with the AGENTS.md rules:

- **Rule 5 (typed interfaces):** Provider interfaces are defined before implementation
- **Rule 6 (modular Python, FastAPI, PostgreSQL, Redis):** This architecture uses all of these
- **Rule 11 (idempotent, recoverable, observable jobs):** Worker design supports this

---

## 6. Related Decisions

- **ADR 0002** (future): Database choice (PostgreSQL confirmed, schema design pending)
- **ADR 0003** (future): Provider interface design
- **ADR 0004** (future): Object storage strategy

---

## 7. Review

This decision should be reviewed if:
- Scale requirements change significantly (millions of streams per day)
- Operational complexity of the monolith becomes burdensome
- A component needs a different technology stack

---

*This ADR follows the format recommended by https://adr.github.io/*
