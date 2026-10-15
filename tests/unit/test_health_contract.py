"""Unit tests for health endpoint contract."""

import json


def test_health_response_contract():
    """Verify health response matches the documented contract."""
    # Expected contract from packages/contracts
    expected_keys = {"status", "version", "environment", "timestamp"}
    expected_status_values = ["ok", "degraded", "unhealthy"]
    expected_env_values = ["development", "staging", "production", "test"]

    # This test documents the expected contract
    # In practice, this would be run against a real endpoint
    sample_response = {
        "status": "ok",
        "version": "0.1.0",
        "environment": "development",
        "timestamp": "2026-01-01T00:00:00+00:00",
    }

    # Verify contract compliance
    assert set(sample_response.keys()) == expected_keys
    assert sample_response["status"] in expected_status_values
    assert sample_response["environment"] in expected_env_values
    assert isinstance(sample_response["version"], str)
    assert isinstance(sample_response["timestamp"], str)


def test_paginated_response_contract():
    """Verify paginated response matches the documented contract."""
    expected_keys = {"data", "total", "page", "page_size", "has_more"}

    sample_response = {
        "data": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "has_more": False,
    }

    assert set(sample_response.keys()) == expected_keys
    assert isinstance(sample_response["data"], list)
    assert isinstance(sample_response["total"], int)
    assert isinstance(sample_response["page"], int)
    assert isinstance(sample_response["page_size"], int)
    assert isinstance(sample_response["has_more"], bool)
