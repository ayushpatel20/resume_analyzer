from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import auth, resumes, analysis, job_roles, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Safely initialize database tables on startup if available
    try:
        init_db()
    except Exception as e:
        print(f"Lifespan init warning: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Full-stack AI Resume Analyzer and Job Matching System (7th Semester B.Tech Mini Project)",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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


@app.get("/", tags=["Root"])
def root():
    """Root landing endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "status": "healthy",
        "documentation": "/docs",
        "health": "/api/health",
    }


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

