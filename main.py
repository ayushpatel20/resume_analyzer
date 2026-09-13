"""
Root-level ASGI entry point for Render deployment.
Adds backend/ to sys.path so 'app' module is importable,
then re-exports the FastAPI app for uvicorn.
"""
import sys
import os

# Ensure backend/ is on the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.main import app  # noqa: F401 — re-exported for uvicorn

__all__ = ["app"]
