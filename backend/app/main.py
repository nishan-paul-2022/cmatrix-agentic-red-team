"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app import __version__, __description__
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.models.responses import RootResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting DeepHat Agent API...")
    logger.info(f"📝 Version: {__version__}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    logger.info(f"🌐 CORS origins: {settings.CORS_ORIGINS}")
    
    # Initialize database
    try:
        from app.core.database import init_db
        logger.info("🗄️  Initializing database...")
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down DeepHat Agent API...")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    # Setup logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description=__description__,
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add GZip middleware for response compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Include API router
    app.include_router(api_router, prefix="/api/v1")
    
    # Root endpoint
    @app.get(
        "/",
        response_model=RootResponse,
        summary="Root Endpoint",
        description="Get API information and available endpoints",
        tags=["Root"]
    )
    async def root() -> RootResponse:
        """Root endpoint with API information."""
        return RootResponse(
            message="DeepHat Agent API is running",
            version=__version__,
            endpoints={
                "health": "/api/v1/health",
                "chat": "/api/v1/chat",
                "stream": "/api/v1/chat/stream",
                "docs": "/docs",
                "redoc": "/redoc",
            }
        )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Handle all unhandled exceptions."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error_code": "INTERNAL_ERROR"
            }
        )
    
    return app


# Create app instance
app = create_application()
