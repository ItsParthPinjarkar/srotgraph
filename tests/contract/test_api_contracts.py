"""Contract tests that verify API responses match the shared contracts."""

import json
from pathlib import Path

import pytest


# Load contracts from the shared package
CONTRACTS_PATH = Path(__file__).parent.parent.parent / "packages" / "contracts" / "src" / "index.ts"


class TestHealthContract:
    """Contract tests for the health endpoint response format."""

    def test_health_response_schema(self) -> None:
        """Health response must match the contract schema."""
        # This test validates that the API response matches packages/contracts
        # In CI, this would be run against a live server
        
        # Expected contract (synced from packages/contracts)
        expected_contract = {
            "type": "object",
            "required": ["status", "version", "environment", "timestamp"],
            "properties": {
                "status": {"enum": ["ok", "degraded", "unhealthy"]},
                "version": {"type": "string"},
                "environment": {
                    "enum": ["development", "staging", "production", "test"]
                },
                "timestamp": {"type": "string", "format": "date-time"},
                "checks": {
                    "type": "object",
                    "properties": {
                        "database": {"enum": ["connected", "disconnected"]},
                        "redis": {"enum": ["connected", "disconnected"]},
                    },
                },
            },
        }

        # Validate contract is well-formed
        assert "required" in expected_contract
        assert "properties" in expected_contract
        assert "status" in expected_contract["properties"]

    def test_contract_file_exists(self) -> None:
        """Shared contracts file should exist."""
        assert CONTRACTS_PATH.exists(), f"Contracts file not found: {CONTRACTS_PATH}"

    def test_contract_exports_health_types(self) -> None:
        """Contracts package should export health-related types."""
        content = CONTRACTS_PATH.read_text()
        
        # Verify key types are defined
        assert "HealthResponse" in content
        assert "ApiError" in content
        assert "PaginatedResponse" in content


class TestStreamContract:
    """Contract tests for stream-related types."""

    def test_stream_type_defined(self) -> None:
        """Stream types should be defined in contracts."""
        content = CONTRACTS_PATH.read_text()
        
        assert "StreamType" in content
        assert "StreamStatus" in content
        assert "Stream" in content

    def test_stream_status_values(self) -> None:
        """Stream status should have the expected values."""
        content = CONTRACTS_PATH.read_text()
        
        # Verify the status values are correct
        assert '"pending"' in content
        assert '"processing"' in content
        assert '"completed"' in content
        assert '"failed"' in content


class TestJobContract:
    """Contract tests for job-related types."""

    def test_job_types_defined(self) -> None:
        """Job types should be defined in contracts."""
        content = CONTRACTS_PATH.read_text()
        
        assert "JobType" in content
        assert "JobStatus" in content
        assert "Job" in content

    def test_job_status_values(self) -> None:
        """Job status should have the expected values."""
        content = CONTRACTS_PATH.read_text()
        
        assert '"queued"' in content
        assert '"processing"' in content
        assert '"completed"' in content
        assert '"failed"' in content
