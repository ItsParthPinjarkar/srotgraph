# SrotGraph Roadmap

**Version:** 1.0.0  
**Status:** Draft  
**Last Updated:** 2026-10-15

---

## 1. Roadmap Overview

This roadmap outlines the planned implementation milestones for SrotGraph. Items are organized by phase, with priorities clearly marked. This is a living document and will be updated as the project progresses.

**Legend:**
- **P0** — Must have for MVP
- **P1** — Important but not blocking
- **P2** — Nice to have, future enhancement

---

## 2. Phase 1: Foundation (Current)

*Goal: Establish the core infrastructure and data model.*

### 2.1 Database Layer (P0)

- [ ] Set up SQLAlchemy models for all entities
- [ ] Create Alembic migration setup
- [ ] Implement initial migration for all tables
- [ ] Set up async database session management
- [ ] Add database health check to API

### 2.2 Core API Endpoints (P0)

- [ ] Streams CRUD (create, list, get, delete)
- [ ] Claims CRUD (create, list, get, update status)
- [ ] Evidence CRUD (create, list, get, verify)
- [ ] Sources CRUD (create, list, get)
- [ ] Relationships CRUD (create, list, get, update status)
- [ ] Job status endpoints
- [ ] Metrics endpoints (basic)

### 2.3 Configuration & Providers (P0)

- [ ] Complete provider interface definitions
- [ ] Implement MockSpeechRecognizer
- [ ] Implement MockClaimExtractor
- [ ] Implement MockEvidenceAnalyzer
- [ ] Wire provider selection via config

### 2.4 Frontend Foundation (P0)

- [ ] Set up project layout and navigation
- [ ] Build API client integration
- [ ] Create dashboard page (list streams)
- [ ] Create stream detail page
- [ ] Create claim review interface

### 2.5 Testing Infrastructure (P0)

- [ ] Set up test database (SQLite for simple tests, PostgreSQL via testcontainers for integration)
- [ ] Write unit tests for services
- [ ] Write integration tests for API endpoints
- [ ] Set up CI workflow (GitHub Actions)

---

## 3. Phase 2: Core Functionality

*Goal: Enable end-to-end stream processing with mock providers.*

### 3.1 Stream Ingestion (P0)

- [ ] File upload endpoint with validation
- [ ] Local file storage for media
- [ ] Transcript storage
- [ ] Async job queuing with Redis Streams
- [ ] Job worker for transcription (mock)
- [ ] Job worker for claim extraction (mock)
- [ ] Progress tracking for jobs

### 3.2 Claim Management (P0)

- [ ] Claim version tracking (edit creates new version)
- [ ] Claim evolution timeline UI
- [ ] Claim status workflow (proposed → validated/rejected)
- [ ] Bulk actions for claims (validate selected, reject selected)

### 3.3 Evidence Management (P1)

- [ ] Upload/attach evidence to claims
- [ ] Evidence verification workflow
- [ ] Evidence list and detail views

### 3.4 Source Management (P1)

- [ ] Source creation and management UI
- [ ] Source reliability tracking
- [ ] Associate streams with sources

---

## 4. Phase 3: Real AI Providers

*Goal: Integrate real AI services for transcription and claim extraction.*

### 4.1 Speech Recognition (P0)

- [ ] Implement Whisper provider (local, open-source)
- [ ] Implement DeepGram provider (cloud)
- [ ] Implement AssemblyAI provider (cloud)
- [ ] Provider comparison/testing
- [ ] Handle provider errors and retries

### 4.2 Claim Extraction (P0)

- [ ] Implement OpenAI provider (GPT-4/GPT-4o)
- [ ] Implement Anthropic provider (Claude)
- [ ] Implement Google provider (Gemini)
- [ ] Prompt engineering for consistent claim extraction
- [ ] Confidence score calibration

### 4.3 Relationship Discovery (P1)

- [ ] AI-suggested relationships between claims
- [ ] Relationship validation workflow
- [ ] Relationship visualization in UI

---

## 5. Phase 4: Metrics & Quality

*Goal: Measure and improve system accuracy and performance.*

### 5.1 Metrics Collection (P0)

- [ ] Automatic metric collection on processing
- [ ] Processing throughput metrics
- [ ] Latency tracking (p50, p95, p99)
- [ ] Memory usage tracking
- [ ] Metrics API and UI dashboards

### 5.2 Accuracy Measurement (P1)

- [ ] Ground truth dataset creation workflow
- [ ] Precision/recall calculation
- [ ] Claim extraction accuracy reporting
- [ ] Relationship extraction accuracy reporting
- [ ] Provider comparison metrics

### 5.3 Information Loss (P2)

- [ ] Measure transcript coverage
- [ ] Measure claim extraction coverage
- [ ] Report information loss metrics

---

## 6. Phase 5: Production Readiness

*Goal: Prepare for production deployment and real users.*

### 6.1 Security (P0)

- [ ] Authentication (session-based for web UI)
- [ ] API key authentication for API access
- [ ] Role-based access control (analyst, verifier, admin)
- [ ] Input validation and sanitization
- [ ] Rate limiting

### 6.2 Deployment (P0)

- [ ] Docker Compose production configuration
- [ ] Environment-specific configurations
- [ ] Secret management documentation
- [ ] Deployment guides for common platforms

### 6.3 Observability (P1)

- [ ] Structured logging (JSON format)
- [ ] Error tracking integration (Sentry or similar)
- [ ] Health check endpoints for load balancer
- [ ] Alerting configuration (future)

### 6.4 Performance (P1)

- [ ] Database query optimization
- [ ] Index optimization based on query patterns
- [ ] Caching layer for frequently accessed data
- [ ] Pagination optimization for large datasets

---

## 7. Phase 6: Advanced Features

*Goal: Add advanced capabilities for power users.*

### 7.1 Advanced Processing (P2)

- [ ] Live stream ingestion
- [ ] Real-time claim extraction
- [ ] Multi-language support
- [ ] Speaker diarization (who said what)

### 7.2 Advanced Analysis (P2)

- [ ] Claim timeline visualization
- [ ] Network graph of claim relationships
- [ ] Source reliability over time
- [ ] Trend analysis across multiple streams

### 7.3 Integrations (P2)

- [ ] Export to common formats (CSV, JSON, PDF reports)
- [ ] Webhook notifications for events
- [ ] Integration with external databases
- [ ] API for programmatic access

---

## 8. Timeline (Estimated)

| Phase | Duration (est.) | Dependencies |
|-------|-----------------|--------------|
| Phase 1: Foundation | 2–3 weeks | None |
| Phase 2: Core Functionality | 3–4 weeks | Phase 1 |
| Phase 3: Real AI Providers | 2–3 weeks | Phase 2 |
| Phase 4: Metrics & Quality | 2–3 weeks | Phase 2, Phase 3 |
| Phase 5: Production Readiness | 2–3 weeks | Phase 1, Phase 2 |
| Phase 6: Advanced Features | Ongoing | Phase 3, Phase 4 |

*These are rough estimates and will be refined as implementation progresses.*

---

## 9. Milestone Summary

| Milestone | Description | Target |
|-----------|-------------|--------|
| M1: Database & API Foundation | Models, migrations, CRUD APIs, mock providers | End of Phase 1 |
| M2: End-to-End Processing | Stream upload, mock processing, claim extraction | End of Phase 2 |
| M3: Real AI Integration | Working with real providers, provider switching | End of Phase 3 |
| M4: Metrics Dashboard | Accuracy, performance, and processing metrics visible | End of Phase 4 |
| M5: Production Ready | Auth, security, deployment guides | End of Phase 5 |

---

## 10. Open Questions for Roadmap

1. **What is the minimum viable accuracy metric?** How do we establish ground truth?
2. **Should we prioritize one AI provider?** Or build all interfaces in parallel?
3. **What is the target user persona for Phase 1?** Solo researcher? Small team?
4. **Is local Whisper viable for the target hardware?** What are the performance characteristics?
5. **Should we build a CLI in addition to the web UI?** For automation use cases?

---

*This roadmap is a planning tool and will be updated as priorities shift and new information becomes available.*
