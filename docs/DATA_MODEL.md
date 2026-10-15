# SrotGraph Data Model

**Version:** 1.0.0  
**Status:** Draft  
**Last Updated:** 2026-10-15

---

## 1. Entity Relationship Overview

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     Source      │       │     Stream      │       │     Claim       │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (UUID)       │       │ id (UUID)       │       │ id (UUID)       │
│ name            │◄──────│ source_id?      │       │ stream_id       │
│ type            │       │ name            │       │ text            │
│ url?            │       │ type            │       │ timestamp_start │
│ reliability?    │       │ status          │       │ timestamp_end   │
│ created_at      │       │ source_url?     │       │ status          │
│ updated_at      │       │ duration?       │       │ confidence      │
│                 │       │ created_at      │       │ source_provider │
│                 │       │ updated_at      │       │ version         │
│                 │       │ error_message?  │       │ parent_claim_id │
│                 │       │ media_path?     │       │ created_at      │
│                 │       │ transcript_path?│      │ updated_at      │
│                 │       │                 │       │ metadata?       │
│                 │       │                 │       │ evidence_ids?   │
│                 │       │                 │       │                 │
│                 │       │                 │       │ parent ─────────┼──┐
│                 │       │                 │       │ children        │  │
│                 │       │                 │       └────────┬────────┘  │
│                 │       │                 │                │           │
│                 │       │                 │       ┌────────┴────────┐  │
│                 │       │                 │       │  ClaimVersion   │  │
│                 │       │                 │       ├─────────────────┤  │
│                 │       │                 │       │ id (UUID)       │  │
│                 │       │                 │       │ claim_id        │◄─┘
│                 │       │                 │       │ version         │
│                 │       │                 │       │ text            │
│                 │       │                 │       │ changed_by      │
│                 │       │                 │       │ change_reason?  │
│                 │       │                 │       │ created_at      │
│                 │       │                 │       └─────────────────┘
│                 │       │                 │
│                 │       │                 │       ┌─────────────────┐
│                 │       │                 │       │     Evidence    │
│                 │       │                 │       ├─────────────────┤
│                 │       │                 │       │ id (UUID)       │
│                 │       │                 │       │ claim_id        │
│                 │       │                 │       │ type            │
│                 │       │                 │       │ content         │
│                 │       │                 │       │ storage_path?   │
│                 │       │                 │       │ source_url?     │
│                 │       │                 │       │ verified        │
│                 │       │                 │       │ verifier?       │
│                 │       │                 │       │ created_at      │
│                 │       │                 │       │ updated_at      │
│                 │       │                 │       └─────────────────┘
│                 │       │                 │
│                 │       │                 │       ┌─────────────────┐
│                 │       │                 │       │ Relationship    │
│                 │       │                 │       ├─────────────────┤
│                 │       │                 │       │ id (UUID)       │
│                 │       │                 │       │ source_claim_id │
│                 │       │                 │       │ target_claim_id │
│                 │       │                 │       │ type            │
│                 │       │                 │       │ confidence      │
│                 │       │                 │       │ status          │
│                 │       │                 │       │ created_at      │
│                 │       │                 │       │ updated_at      │
│                 │       │                 │       └─────────────────┘
│                 │       │                 │
│                 │       │                 │       ┌─────────────────┐
│                 │       │                 │       │     Job         │
│                 │       │                 │       ├─────────────────┤
│                 │       │                 │       │ id (UUID)       │
│                 │       │                 │       │ stream_id       │
│                 │       │                 │       │ type            │
│                 │       │                 │       │ status          │
│                 │       │                 │       │ progress        │
│                 │       │                 │       │ result?         │
│                 │       │                 │       │ error?          │
│                 │       │                 │       │ created_at      │
│                 │       │                 │       │ started_at?     │
│                 │       │                 │       │ completed_at?   │
│                 │       │                 │       └─────────────────┘
│                 │       │                 │
│                 │       │                 │       ┌─────────────────┐
│                 │       │                 │       │    Metric       │
│                 │       │                 │       ├─────────────────┤
│                 │       │                 │       │ id (UUID)       │
│                 │       │                 │       │ name            │
│                 │       │                 │       │ value           │
│                 │       │                 │       │ category        │
│                 │       │                 │       │ created_at      │
│                 │       │                 │       └─────────────────┘
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

---

## 2. Entity Definitions

### 2.1 Stream

Represents an audio, video, or text stream that has been ingested for processing.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `name` | VARCHAR(255) | Human-readable name |
| `type` | VARCHAR(20) | `audio`, `video`, or `text` |
| `status` | VARCHAR(20) | `pending`, `processing`, `completed`, `failed` |
| `source_url` | VARCHAR(2048) | Optional source URL |
| `duration_seconds` | INTEGER | Duration in seconds (if applicable) |
| `media_path` | VARCHAR(500) | Path to stored media file |
| `transcript_path` | VARCHAR(500) | Path to stored transcript |
| `error_message` | TEXT | Error details if processing failed |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

**Indexes:**
- `idx_stream_status` on `status`
- `idx_stream_created_at` on `created_at`
- `idx_stream_type` on `type`

**Relationships:**
- Has many Claims (one-to-many)
- Has many Jobs (one-to-many)

---

### 2.2 Claim

A timestamped assertion extracted from a stream.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `stream_id` | UUID (FK → Stream) | Source stream |
| `text` | TEXT | The claim text |
| `timestamp_start` | NUMERIC(10,2) | Start time in seconds |
| `timestamp_end` | NUMERIC(10,2) | End time in seconds |
| `status` | VARCHAR(20) | `proposed`, `validated`, `rejected`, `pending_review` |
| `confidence` | NUMERIC(3,2) | AI confidence score (0.00–1.00) |
| `source_provider` | VARCHAR(100) | Which AI provider extracted this |
| `version` | INTEGER | Current version number (starts at 1) |
| `parent_claim_id` | UUID (FK → Claim, nullable) | For claim evolution tracking |
| `metadata` | JSONB | Additional metadata |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

**Indexes:**
- `idx_claim_stream_id` on `stream_id`
- `idx_claim_status` on `status`
- `idx_claim_parent` on `parent_claim_id`
- `idx_claim_timestamps` on `(stream_id, timestamp_start, timestamp_end)`
- `idx_claim_created_at` on `created_at`

**Relationships:**
- Belongs to Stream (many-to-one)
- Has many ClaimVersions (one-to-many)
- Has many Evidence (one-to-many)
- Has many Relationships where it is source (one-to-many)
- Has many Relationships where it is target (one-to-many)
- Has many children Claims (self-referential)

---

### 2.3 ClaimVersion

Historical versions of a claim when it is edited.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `claim_id` | UUID (FK → Claim) | The claim this version belongs to |
| `version` | INTEGER | Version number |
| `text` | TEXT | Claim text at this version |
| `changed_by` | VARCHAR(255) | Who/what made the change |
| `change_reason` | TEXT | Optional reason for the change |
| `created_at` | TIMESTAMPTZ | When this version was created |

**Indexes:**
- `idx_version_claim_id` on `claim_id`
- `idx_version_number` on `(claim_id, version)`

**Note:** The `Claim.text` column always holds the current version. Previous versions are in this table.

---

### 2.4 Evidence

Supporting material attached to a claim.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `claim_id` | UUID (FK → Claim) | Associated claim |
| `type` | VARCHAR(20) | `transcript`, `snapshot`, `metadata`, `reference` |
| `content` | TEXT | Evidence content (for text-based evidence) |
| `storage_path` | VARCHAR(500) | Path to stored artifact (for files) |
| `source_url` | VARCHAR(2048) | URL of external reference |
| `verified` | BOOLEAN | Whether evidence has been verified |
| `verifier` | VARCHAR(255) | Who verified the evidence |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

**Indexes:**
- `idx_evidence_claim_id` on `claim_id`
- `idx_evidence_type` on `type`
- `idx_evidence_verified` on `verified`

---

### 2.5 Source

Origin of content or claims.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `name` | VARCHAR(255) | Source name |
| `type` | VARCHAR(20) | `human`, `feed`, `database`, `api` |
| `url` | VARCHAR(2048) | Optional URL |
| `reliability_score` | NUMERIC(3,2) | Reliability score (0.00–1.00) |
| `metadata` | JSONB | Additional metadata |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

**Indexes:**
- `idx_source_type` on `type`
- `idx_source_reliability` on `reliability_score`

**Relationships:**
- Has many Streams (one-to-many)

---

### 2.6 Relationship

Connections between claims.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `source_claim_id` | UUID (FK → Claim) | Source claim |
| `target_claim_id` | UUID (FK → Claim) | Target claim |
| `type` | VARCHAR(20) | `supports`, `contradicts`, `corroborates`, `related_to` |
| `confidence` | NUMERIC(3,2) | AI confidence score (0.00–1.00) |
| `status` | VARCHAR(20) | `proposed`, `validated`, `rejected` |
| `metadata` | JSONB | Additional metadata |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

**Constraints:**
- CHECK: `source_claim_id != target_claim_id` (no self-relationships)

**Indexes:**
- `idx_rel_source` on `source_claim_id`
- `idx_rel_target` on `target_claim_id`
- `idx_rel_type` on `type`
- `idx_rel_status` on `status`

**Note:** Relationships are directional. If claim A "supports" claim B, there is a relationship from A → B.

---

### 2.7 Job

Async processing job.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `stream_id` | UUID (FK → Stream) | Associated stream |
| `type` | VARCHAR(30) | `transcription`, `claim_extraction`, `evidence_analysis` |
| `status` | VARCHAR(20) | `queued`, `processing`, `completed`, `failed` |
| `progress` | INTEGER | Progress percentage (0–100) |
| `result` | TEXT | Result data (JSON string) |
| `error_message` | TEXT | Error details if failed |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `started_at` | TIMESTAMPTZ | When processing started |
| `completed_at` | TIMESTAMPTZ | When processing completed |

**Indexes:**
- `idx_job_stream_id` on `stream_id`
- `idx_job_status` on `status`
- `idx_job_type` on `type`
- `idx_job_created_at` on `created_at`

---

### 2.8 Metric

Collected metrics for monitoring and analysis.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID (PK) | Unique identifier |
| `name` | VARCHAR(100) | Metric name (e.g., "claim_precision") |
| `value` | NUMERIC(10,4) | Metric value |
| `category` | VARCHAR(30) | `processing`, `accuracy`, `performance` |
| `metadata` | JSONB | Additional context |
| `created_at` | TIMESTAMPTZ | When metric was recorded |

**Indexes:**
- `idx_metric_name` on `name`
- `idx_metric_category` on `category`
- `idx_metric_created_at` on `created_at`

---

## 3. Entity Relationships

### 3.1 Relationship Table

| From | To | Type | Cardinality | Description |
|------|-----|------|-------------|-------------|
| Source | Stream | Foreign Key | One-to-Many | A source can have many streams |
| Stream | Claim | Foreign Key | One-to-Many | A stream can have many claims |
| Stream | Job | Foreign Key | One-to-Many | A stream can have many jobs |
| Claim | ClaimVersion | Foreign Key | One-to-Many | A claim has many versions |
| Claim | Evidence | Foreign Key | One-to-Many | A claim can have many evidence items |
| Claim | Claim | Self-Reference | One-to-Many | A claim can have child claims (evolution) |
| Claim | Relationship | Foreign Key | One-to-Many (source) | A claim can be the source of many relationships |
| Claim | Relationship | Foreign Key | One-to-Many (target) | A claim can be the target of many relationships |

---

## 4. Data Retention

### 4.1 Retention Policy (Proposed)

| Data Type | Retention | Rationale |
|-----------|-----------|-----------|
| Streams (metadata) | Indefinite | Historical record |
| Media files | Configurable | Storage costs may require archiving |
| Transcripts | Indefinite | Evidence chain |
| Claims | Indefinite | Historical record, never overwritten |
| ClaimVersions | Indefinite | Full audit trail |
| Evidence | Indefinite | Evidence chain |
| Jobs | 90 days | Operational, not historical |
| Metrics | Indefinite | Trend analysis |

*Note: Specific retention policies should be configurable and may vary by deployment.*

---

## 5. Design Decisions

### 5.1 Why UUIDs?

- Distributed-friendly (no coordination needed for ID generation)
- Unpredictable (security through obscurity is not the goal, but it helps)
- Can be generated client-side or in workers without DB round-trip

### 5.2 Why JSONB for Metadata?

- Flexible schema for varying data without migrations
- Queryable in PostgreSQL
- Can be indexed if needed

### 5.3 Why Separate ClaimVersion Table?

- Preserves full history without modifying the main Claim row
- Allows querying specific versions
- Clean separation between current state and history

### 5.4 Why Numeric for Timestamps?

- Precision to 0.01 seconds (centisecond) is sufficient for media
- Avoids floating-point comparison issues
- Easy to convert to/from float in application code

---

## 6. Schema Migration Plan

Migrations will be managed with Alembic. Initial migration sequence:

1. Create tables in dependency order (no FK deps first)
2. Add indexes after data insertion where possible
3. Add constraints after data validation

See `backend/alembic/` for migration files (to be created).

---

*This data model will evolve as features are added. Changes should be reflected in Alembic migrations and updated in this document.*
