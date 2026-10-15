/**
 * @srotgraph/contracts
 *
 * Versioned shared data contracts between frontend and backend.
 * These types define the API boundary and should be kept in sync.
 *
 * Version: 1.0.0
 */

// ============================================================================
// Health
// ============================================================================

export interface HealthResponse {
  status: "ok" | "degraded" | "unhealthy";
  version: string;
  environment: "development" | "staging" | "production" | "test";
  timestamp: string;
  checks?: {
    database?: "connected" | "disconnected";
    redis?: "connected" | "disconnected";
  };
}

// ============================================================================
// API Error
// ============================================================================

export interface ApiError {
  detail: string;
  status_code: number;
  errors?: Record<string, string[]>;
}

// ============================================================================
// Pagination
// ============================================================================

export interface PaginationParams {
  page: number;
  page_size: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

// ============================================================================
// Stream
// ============================================================================

export type StreamType = "audio" | "video" | "text";
export type StreamStatus = "pending" | "processing" | "completed" | "failed";

export interface Stream {
  id: string;
  name: string;
  type: StreamType;
  status: StreamStatus;
  source_url?: string;
  duration_seconds?: number;
  media_path?: string;
  transcript_path?: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateStreamRequest {
  name: string;
  type: StreamType;
  source_url?: string;
}

export interface StreamListQueryParams {
  page?: number;
  page_size?: number;
  status?: StreamStatus;
  type?: StreamType;
}

// ============================================================================
// Job
// ============================================================================

export type JobType = "transcription" | "claim_extraction" | "evidence_analysis";
export type JobStatus = "queued" | "processing" | "completed" | "failed";

export interface Job {
  id: string;
  stream_id: string;
  type: JobType;
  status: JobStatus;
  progress: number;
  result?: string;
  error_message?: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}
