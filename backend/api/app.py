from contextlib import asynccontextmanager
from anyio import to_thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import events, performances, base
from api.loader import load_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context: pre-load events at startup.

    Uses anyio.to_thread.run_sync to run the blocking loader without
    blocking the event loop.
    """
    try:
        ok = await to_thread.run_sync(load_events)
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
app.include_router(base.router)
app.include_router(events.router)
app.include_router(performances.router)
