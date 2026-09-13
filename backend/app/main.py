from __future__ import annotations
import os
import sys
from pathlib import Path

# ── sys.path bootstrap (works for Render, Vercel, local) ──────────────────
_app_dir = Path(__file__).resolve().parent      # backend/app/
_backend_dir = _app_dir.parent                  # backend/
_root_dir = _backend_dir.parent                 # project root

for _p in [_backend_dir, _root_dir, _app_dir,
           Path("/var/task"), Path("/var/task/backend")]:
    if _p.exists() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db
from app.routers import auth, resumes, analysis, job_roles, reports

# ── Initialize database on startup ─────────────────────────────────────────
try:
    init_db()
except Exception as _e:
    print(f"[WARN] DB init error (will retry on first request): {_e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Full-stack AI Resume Analyzer and Job Matching System (7th Semester B.Tech Mini Project)",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ────────────────────────────────────────────────────────────────────
# Allow all origins so the app works on any Render/Vercel/local URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health Check (first, fastest route) ────────────────────────────────────
@app.get("/api/health", tags=["Health"])
@app.get("/health", tags=["Health"])
def health_check():
    """Zero-overhead health check for Render's health-check ping."""
    return {"status": "healthy", "service": settings.PROJECT_NAME}


# ── API Routers ─────────────────────────────────────────────────────────────
app.include_router(auth.router,       prefix=settings.API_V1_STR)
app.include_router(resumes.router,    prefix=settings.API_V1_STR)
app.include_router(analysis.router,   prefix=settings.API_V1_STR)
app.include_router(job_roles.router,  prefix=settings.API_V1_STR)
app.include_router(reports.router,    prefix=settings.API_V1_STR)


# ── Resolve the React dist/ directory ──────────────────────────────────────
_dist_candidates = [
    _app_dir / "dist",          # backend/app/dist  ← set by render-build.sh
    _backend_dir / "dist",      # backend/dist
    _root_dir / "dist",         # project root dist
    _root_dir / "frontend" / "dist",
    Path("/var/task/app/dist"),
    Path("/var/task/dist"),
]
_dist_dir: Path | None = None
for _d in _dist_candidates:
    if (_d / "index.html").exists():
        _dist_dir = _d
        break

if _dist_dir:
    # Mount static assets (JS/CSS bundles) — must be before catch-all
    _assets = _dist_dir / "assets"
    if _assets.exists():
        app.mount("/assets", StaticFiles(directory=str(_assets)), name="assets")
    print(f"[INFO] Serving React frontend from: {_dist_dir}")
else:
    print("[WARN] React dist/ not found — API-only mode.")


# ── SPA Root & Catch-all ────────────────────────────────────────────────────
@app.get("/", tags=["Frontend"])
def root():
    """Serve the React SPA index.html."""
    if _dist_dir and (_dist_dir / "index.html").exists():
        return FileResponse(str(_dist_dir / "index.html"))
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/{full_path:path}", tags=["Frontend"])
def spa_catch_all(full_path: str):
    """Serve SPA routes; let the React router handle client-side navigation."""
    # Don't intercept API routes
    if full_path.startswith("api/") or full_path in ("api", "docs", "redoc"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    if _dist_dir:
        # Serve existing static file (favicon, manifest, etc.)
        static_file = _dist_dir / full_path
        if static_file.is_file():
            return FileResponse(str(static_file))
        # Fall back to index.html for React Router routes
        idx = _dist_dir / "index.html"
        if idx.exists():
            return FileResponse(str(idx))

    return JSONResponse(status_code=404, content={"detail": "Not found"})


# Expose ASGI handler for serverless adapters (Vercel etc.)
handler = app
