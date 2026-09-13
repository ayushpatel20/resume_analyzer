from __future__ import annotations
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add backend and root directories to sys.path so 'app' imports seamlessly in any environment
_app_dir = Path(__file__).resolve().parent
_backend_dir = _app_dir.parent
_root_dir = _backend_dir.parent
for _p in [_backend_dir, _root_dir, _app_dir, Path("/var/task"), Path("/var/task/backend")]:
    if _p.exists() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db
from app.routers import auth, resumes, analysis, job_roles, reports


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Full-stack AI Resume Analyzer and Job Matching System (7th Semester B.Tech Mini Project)",
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS Configuration for local React Vite frontend and production deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Minimal Health Check Endpoints defined FIRST for immediate serverless invocation
@app.get("/api/health", tags=["Health"])
@app.get("/health", tags=["Health"])
def health_check():
    """Minimal health check endpoint for zero-overhead verification of backend status."""
    return {"status": "healthy"}


# Register Routers (both with /api and direct in case Vercel rewrites strip the prefix)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(resumes.router, prefix=settings.API_V1_STR)
app.include_router(analysis.router, prefix=settings.API_V1_STR)
app.include_router(job_roles.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)

# Direct routes fallback
app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(analysis.router)
app.include_router(job_roles.router)
app.include_router(reports.router)

# Resolve dist directory for static files and SPA serving
_dist_candidates = [
    _app_dir / "dist",
    _backend_dir / "dist",
    _root_dir / "dist",
    Path("/var/task/app/dist"),
    Path("/var/task/dist"),
    Path("/var/task/backend/dist"),
]
_dist_dir: Path | None = None
for _d in _dist_candidates:
    if (_d / "index.html").exists():
        _dist_dir = _d
        break


if _dist_dir and (_dist_dir / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(_dist_dir / "assets")), name="assets")


@app.get("/", tags=["Root"])
def root():
    """Serve React frontend index.html if available, else return status."""
    if _dist_dir and (_dist_dir / "index.html").exists():
        return FileResponse(str(_dist_dir / "index.html"))
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "status": "healthy",
        "documentation": "/docs",
        "health": "/api/health",
    }


@app.get("/{full_path:path}")
def catch_all_spa(full_path: str):
    """Serve SPA routes or static files for frontend routing."""
    if full_path.startswith("api/") or full_path == "api":
        return JSONResponse(status_code=404, content={"detail": "API route not found"})
    if _dist_dir:
        static_file = _dist_dir / full_path
        if static_file.is_file():
            return FileResponse(str(static_file))
        index_file = _dist_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
    return JSONResponse(status_code=404, content={"detail": "Not found"})


# Expose handler for Vercel Serverless Function runtime
handler = app
