from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_client import CONTENT_TYPE_LATEST

from .config import get_settings
from .api import incidents, ingestion, websocket
from .observability.metrics import get_metrics

# Initialize settings
settings = get_settings()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Real-time AI system for incident detection and response",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - configurable via environment
allowed_origins = settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(incidents.router)
app.include_router(ingestion.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with component status"""
    from .db.storage import storage
    from .ai.commander import ai_commander

    health_status = {
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "storage": "operational",
            "ai_commander": "operational" if ai_commander.enabled else "fallback_mode",
        }
    }

    # Check if we have any incidents in storage
    try:
        incidents_count = len(storage.incidents)
        health_status["metrics"] = {
            "total_incidents": incidents_count
        }
    except Exception:
        health_status["components"]["storage"] = "degraded"
        health_status["status"] = "degraded"

    return health_status


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=get_metrics(),
        media_type=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
