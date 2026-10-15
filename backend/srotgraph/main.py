"""SrotGraph FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from srotgraph.config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="SrotGraph API",
        description="Evidence-preserving intelligence system API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.is_development else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers here as we build out the API
    # from srotgraph.routes import streams, claims, evidence
    # app.include_router(streams.router, prefix=settings.api_prefix)
    # app.include_router(claims.router, prefix=settings.api_prefix)
    # app.include_router(evidence.router, prefix=settings.api_prefix)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok", "env": settings.app_env}

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint with API info."""
        return {
            "name": "SrotGraph API",
            "version": "0.1.0",
            "docs": "/docs",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("srotgraph.main:app", host="0.0.0.0", port=8000, reload=settings.is_development)
