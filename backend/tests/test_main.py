"""Tests for the main application."""
import pytest
from fastapi.testclient import TestClient

from srotgraph.main import app


@pytest.fixture
def client():
    """Create a test client for the application."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_ok(self, client: TestClient) -> None:
        """Health check should return status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "env" in data

    def test_health_check_has_env(self, client: TestClient) -> None:
        """Health check should include environment info."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["env"] in ("development", "production", "test")


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_api_info(self, client: TestClient) -> None:
        """Root endpoint should return API name and version."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "SrotGraph API"
        assert data["version"] == "0.1.0"
        assert data["docs"] == "/docs"


class TestDocsEndpoint:
    """Tests for the API documentation endpoint."""

    def test_docs_available(self, client: TestClient) -> None:
        """Swagger docs should be available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self, client: TestClient) -> None:
        """ReDoc documentation should be available."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema_available(self, client: TestClient) -> None:
        """OpenAPI schema should be available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
