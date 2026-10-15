/**
 * SrotGraph API Type Definitions
 *
 * These types define the data contracts between the frontend and backend.
 * All AI-generated claims and relationships are treated as uncertain proposals
 * until validated by human review.
 */

// ============================================================================
// Stream Processing
// ============================================================================

export interface Stream {
  id: string;
  name: string;
  type: "audio" | "video" | "text";
  status: "pending" | "processing" | "completed" | "failed";
  created_at: string;
  updated_at: string;
  duration_seconds?: number;
  error_message?: string;
}

export interface StreamInput {
  name: string;
  type: "audio" | "video" | "text";
  source_url?: string;
  file?: File;
}

// ============================================================================
// Claims
// ============================================================================

export type ClaimStatus = "proposed" | "validated" | "rejected" | "pending_review";

export interface Claim {
  id: string;
  stream_id: string;
  text: string;
  timestamp_start: number; // seconds
  timestamp_end: number;   // seconds
  status: ClaimStatus;
  confidence: number;      // 0.0 - 1.0
  source_provider: string;
  created_at: string;
  updated_at: string;
  version: number;
  parent_claim_id?: string; // For claim evolution tracking
  evidence_ids?: string[];
  metadata?: Record<string, unknown>;
}

export interface ClaimInput {
  stream_id: string;
  text: string;
  timestamp_start: number;
  timestamp_end: number;
  confidence: number;
  source_provider: string;
  parent_claim_id?: string;
  metadata?: Record<string, unknown>;
}

export interface ClaimEvolution {
  claim_id: string;
  versions: ClaimVersion[];
  current_version: number;
}

export interface ClaimVersion {
  version: number;
  text: string;
  timestamp: string;
  changed_by: string;
  change_reason?: string;
  previous_text?: string;
}

// ============================================================================
// Evidence
// ============================================================================

export type EvidenceType = "transcript" | "snapshot" | "metadata" | "reference";

export interface Evidence {
  id: string;
  claim_id: string;
  type: EvidenceType;
  content: string;
  source_url?: string;
  created_at: string;
  verified: boolean;
  verifier?: string;
}

export interface EvidenceInput {
  claim_id: string;
  type: EvidenceType;
  content: string;
  source_url?: string;
}

// ============================================================================
// Sources
// ============================================================================

export interface Source {
  id: string;
  name: string;
  type: "human" | "feed" | "database" | "api";
  url?: string;
  reliability_score?: number; // 0.0 - 1.0
  created_at: string;
  claims_count: number;
}

export interface SourceInput {
  name: string;
  type: "human" | "feed" | "database" | "api";
  url?: string;
  reliability_score?: number;
}

// ============================================================================
// Relationships
// ============================================================================

export type RelationshipType = "supports" | "contradicts" | "corroborates" | "related_to";

export interface Relationship {
  id: string;
  source_claim_id: string;
  target_claim_id: string;
  type: RelationshipType;
  confidence: number;
  created_at: string;
  status: "proposed" | "validated" | "rejected";
}

export interface RelationshipInput {
  source_claim_id: string;
  target_claim_id: string;
  type: RelationshipType;
  confidence: number;
}

// ============================================================================
// Metrics
// ============================================================================

export interface ProcessingMetrics {
  total_streams: number;
  processing_time_seconds: number;
  claims_extracted: number;
  claims_validated: number;
  claims_rejected: number;
  evidence_collected: number;
  relationships_identified: number;
}

export interface AccuracyMetrics {
  claim_precision: number;
  claim_recall: number;
  relationship_precision: number;
  relationship_recall: number;
  evidence_verification_rate: number;
}

export interface PerformanceMetrics {
  latency_p50_ms: number;
  latency_p95_ms: number;
  latency_p99_ms: number;
  memory_usage_mb: number;
  throughput_streams_per_hour: number;
}

// ============================================================================
// API Responses
// ============================================================================

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  error?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

// ============================================================================
// Job Status (for async processing)
// ============================================================================

export type JobStatus = "queued" | "processing" | "completed" | "failed";

export interface Job {
  id: string;
  type: "transcription" | "claim_extraction" | "evidence_analysis";
  status: JobStatus;
  progress: number; // 0-100
  result?: string;
  error?: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}
