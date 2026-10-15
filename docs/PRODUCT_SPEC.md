# SrotGraph Product Specification

**Version:** 1.0.0  
**Status:** Draft  
**Last Updated:** 2026-10-15

---

## 1. Problem Statement

Intelligence analysts, researchers, and content moderators face a growing challenge: they must process large volumes of audio, video, and text content to extract meaningful claims, verify their accuracy, track how those claims evolve over time, and connect them to supporting or contradictory evidence.

Current tools tend to focus on either:
- **Transcription** (speech-to-text) without semantic understanding
- **Chat-based Q&A** without persistent evidence trails
- **Fact-checking databases** without real-time stream processing

There is no integrated system that preserves the full evidence chain from raw media to validated claims with measurable accuracy metrics.

### Core Problems to Solve

1. **Claim Extraction**: Automatically identify factual assertions in streaming or recorded media
2. **Evidence Preservation**: Maintain immutable records linking claims to their source material
3. **Claim Evolution Tracking**: Track how claims are refined, contested, or updated over time
4. **Source Connection**: Link claims to their originating sources and assess source reliability
5. **Metrics & Observability**: Measure accuracy, latency, memory usage, and information loss

---

## 2. User Workflows

### 2.1 Stream Ingestion Workflow

**Actor:** Content analyst, researcher, automated pipeline

1. User uploads or configures a stream (audio file, video file, text feed, or live stream URL)
2. System validates the input and creates a Stream record with status `pending`
3. System queues async processing jobs for transcription and claim extraction
4. User can monitor progress via job status endpoints
5. Upon completion, stream status changes to `completed` with extracted claims available

### 2.2 Claim Review Workflow

**Actor:** Analyst, verifier

1. User views extracted claims for a stream, sorted by timestamp
2. Each claim displays:
   - Original text
   - Timestamp range in source media
   - Confidence score from AI provider
   - Current status (proposed/validated/rejected)
   - Linked evidence (if any)
3. User can:
   - **Validate** a claim (mark as verified)
   - **Reject** a claim (mark as inaccurate)
   - **Edit** claim text (creates a new version, preserves history)
   - **Add evidence** (link transcript segments, external references, metadata)
   - **Create relationships** to other claims (supports, contradicts, corroborates)

### 2.3 Evidence Collection Workflow

**Actor:** Automated pipeline, analyst

1. For each claim, system can attach:
   - **Transcript segments**: The exact text surrounding the claim in the source
   - **Media snapshots**: Key frames from video at claim timestamp
   - **Metadata**: Technical metadata from the source file
   - **External references**: URLs, document IDs, database records
2. Evidence can be marked as `verified` or `unverified`
3. Verified evidence contributes to claim confidence scoring

### 2.4 Claim Evolution Workflow

**Actor:** Analyst, automated system

1. When a claim is edited, the previous version is preserved
2. Each version records:
   - The text at that version
   - Timestamp of change
   - Who/what made the change
   - Reason for change (optional)
3. Users can view the full evolution timeline for any claim
4. Parent-child relationships between claims track derived or updated claims

### 2.5 Metrics & Reporting Workflow

**Actor:** System operator, researcher

1. System continuously collects:
   - **Processing metrics**: Streams processed, time taken, throughput
   - **Accuracy metrics**: Precision/recall against validated ground truth
   - **Performance metrics**: Latency percentiles, memory usage
2. Metrics are exposed via API for dashboards and analysis
3. Information loss is measured by comparing extracted claims against source content

---

## 3. User Roles & Permissions

| Role | Capabilities |
|------|-------------|
| **Analyst** | View streams, claims, evidence; validate/reject claims; add evidence; create relationships |
| **Verifier** | Same as Analyst, plus can verify evidence |
| **Administrator** | All capabilities, plus manage sources, configure providers, view system metrics |
| **API Client** | Programmatic access via API keys (future) |

*Note: Role-based access control is planned but not yet implemented. Initial version may have simpler authentication.*

---

## 4. Functional Requirements

### 4.1 Stream Processing (Priority: High)

- [ ] Upload audio files (MP3, WAV, M4A, etc.)
- [ ] Upload video files (MP4, MKV, etc.) — extract audio for processing
- [ ] Ingest text streams (RSS feeds, API endpoints, uploaded text)
- [ ] Support live stream URLs (future)
- [ ] Track processing status: pending, processing, completed, failed
- [ ] Store stream metadata: name, type, duration, source URL, created/updated timestamps

### 4.2 Speech Recognition (Priority: High)

- [ ] Pluggable provider interface
- [ ] Support for Whisper (local), DeepGram, AssemblyAI (cloud)
- [ ] Mock provider for testing (returns deterministic data)
- [ ] Configurable via environment variables
- [ ] Preserve full transcript with timestamps
- [ ] Handle provider failures gracefully with retries

### 4.3 Claim Extraction (Priority: High)

- [ ] Pluggable provider interface
- [ ] Support for OpenAI, Anthropic, Google (cloud)
- [ ] Mock provider for testing
- [ ] Extract timestamped claims from transcript/text
- [ ] Each claim has: text, start time, end time, confidence, source provider
- [ ] Claims are initially `proposed` status

### 4.4 Claim Management (Priority: High)

- [ ] List claims by stream, with pagination
- [ ] Get single claim with full details
- [ ] Update claim status (proposed → validated/rejected)
- [ ] Edit claim text (creates new version, preserves history)
- [ ] Track claim versions with change history
- [ ] Support parent-child relationships for claim evolution

### 4.5 Evidence Management (Priority: Medium)

- [ ] Attach evidence to claims
- [ ] Evidence types: transcript, snapshot, metadata, reference
- [ ] Verify/unverify evidence
- [ ] Track who verified evidence and when

### 4.6 Source Management (Priority: Medium)

- [ ] Register sources (human, feed, database, API)
- [ ] Track source reliability scores
- [ ] Associate claims with sources
- [ ] Count claims per source

### 4.7 Relationship Discovery (Priority: Medium)

- [ ] AI-suggested relationships between claims
- [ ] Relationship types: supports, contradicts, corroborates, related_to
- [ ] Relationships start as `proposed`, can be validated/rejected
- [ ] Confidence scoring for relationships

### 4.8 Metrics & Monitoring (Priority: Medium)

- [ ] Processing throughput metrics
- [ ] Accuracy metrics (precision, recall)
- [ ] Latency tracking (p50, p95, p99)
- [ ] Memory usage tracking
- [ ] Information loss measurement

### 4.9 Async Job Processing (Priority: High)

- [ ] Redis Streams for job queue
- [ ] Idempotent job processing
- [ ] Job status tracking: queued, processing, completed, failed
- [ ] Progress reporting (0-100%)
- [ ] Retry logic for failed jobs
- [ ] Observable via logs and metrics

---

## 5. Non-Functional Requirements

### 5.1 Security

- API credentials via environment variables only (never hardcoded)
- No private media or credentials in logs
- Secure handling of uploaded files
- Authentication planned for future (not in initial scope)

### 5.2 Reliability

- All background jobs must be idempotent
- Failed jobs must be retryable
- Processing must be recoverable after interruption
- No silent data loss or overwrites of accepted history

### 5.3 Observability

- Structured logging
- Metrics exported for monitoring
- Job status visible via API
- Health check endpoint

### 5.4 Performance

- Async processing to avoid blocking API responses
- Streaming responses where applicable
- Efficient database queries with proper indexing

---

## 6. Out of Scope (Initial Version)

- User authentication and authorization (planned, not initial)
- Live stream ingestion (future)
- Real-time claim updates via WebSocket (future)
- Multi-tenant isolation (future)
- Geographic distribution (future)
- Mobile applications (future)

---

## 7. Success Criteria

1. System can ingest an audio/video/text stream and extract timestamped claims
2. Claims can be reviewed, validated, rejected, and edited with full history
3. Evidence can be attached and verified
4. Relationships between claims can be created and tracked
5. Metrics are collected and accessible
6. All AI providers are interchangeable via configuration
7. Tests pass without requiring paid API access
8. System runs locally via Docker Compose

---

## 8. Assumptions

1. **Audio processing is the primary initial use case** — video is handled by extracting audio
2. **Mock providers are sufficient for initial development** — real providers added later
3. **PostgreSQL is the correct choice** for metadata storage (relational, ACID, mature)
4. **Redis Streams is appropriate** for job queue (simple, well-understood)
5. **Object storage for media** will use local filesystem initially, possibly cloud storage later
6. **Single-user/single-tenant initially** — multi-tenancy is future work
7. **Accuracy measurement requires ground truth** — initially manual, possibly semi-automated later

---

## 9. Open Questions

1. What is the minimum viable accuracy metric? How do we get ground truth without manual labeling?
2. Should claim extraction be batched (process entire transcript) or streaming (incremental)?
3. What is the appropriate granularity for evidence snapshots in video?
4. How do we handle claims that span multiple timestamps or are implied rather than stated?
5. What is the retention policy for raw media vs. extracted data?

---

*This specification will evolve as the project progresses. Updates should be reflected in the ROADMAP.md and relevant architecture decision records.*
