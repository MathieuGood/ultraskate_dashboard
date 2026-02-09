"""
Entry point for running the FastAPI server.

Run with: uv run uvicorn api.main:app --reload
"""

from api.app import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
