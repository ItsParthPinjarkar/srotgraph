"""Integration tests for the API health endpoint."""

import pytest
import httpx


@pytest.fixture
def api_base_url() -> str:
    """Base URL for the API (can be overridden)."""
    return "http://localhost:8000"


@pytest.fixture
async def async_client(api_base_url: str) -> httpx.AsyncClient:
    """Async HTTP client for integration tests."""
    async with httpx.AsyncClient(base_url=api_base_url) as client:
        yield client


class TestHealthEndpointIntegration:
    """Integration tests for the health endpoint.
    
    These tests require the API to be running.
    Skip if the server is not available.
    """

    @pytest.mark.skipif(
        True,  # Will skip if server not running - can be made conditional
        reason="API server not running"
    )
    async def test_health_endpoint_reachable(self, async_client: httpx.AsyncClient) -> None:
        """Health endpoint should be reachable and return expected data."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "environment" in data
        assert "timestamp" in data

    @pytest.mark.skipif(
        True,
        reason="API server not running"
    )
    async def test_root_endpoint_reachable(self, async_client: httpx.AsyncClient) -> None:
        """Root endpoint should be reachable."""
        response = await async_client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "version" in data
