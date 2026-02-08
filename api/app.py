"""FastAPI application for UltraskateDashboard"""

from contextlib import asynccontextmanager
import anyio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import events, performances
from api.loader import load_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context: pre-load events at startup.

    Uses anyio.to_thread.run_sync to run the blocking loader without
    blocking the event loop.
    """
    try:
        ok = await anyio.to_thread.run_sync(load_events)
        print(f"Startup: events loaded -> {ok}")
    except Exception as e:
        print(f"Startup: failed to load events: {e}")
    yield


app = FastAPI(
    title="UltraskateDashboard API",
    description="API for skateboard race event tracking and analysis",
    version="0.1.0",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events.router)
app.include_router(performances.router)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "UltraskateDashboard API",
        "version": "0.1.0",
        "status": "online",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
