import os
import sys
from pathlib import Path

# Ensure VERCEL environment flag is set
os.environ["VERCEL"] = "1"

# Dynamically locate and prepend paths where 'app' might reside
curr_file = Path(__file__).resolve()
possible_dirs = [
    curr_file.parent.parent / "backend",
    curr_file.parent / "backend",
    curr_file.parent.parent,
    curr_file.parent,
    Path("/var/task/backend"),
    Path("/var/task"),
]

for p in possible_dirs:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from app.main import app
except Exception as exc:
    import traceback
    traceback.print_exc()

    # Diagnostic ASGI fallback to expose exact error instead of opaque FUNCTION_INVOCATION_FAILED
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="Diagnostic Fallback")

    @app.get("/api/health")
    @app.get("/health")
    def fallback_health():
        return {
            "status": "diagnostic_mode",
            "error": f"{type(exc).__name__}: {str(exc)}",
            "traceback": traceback.format_exc(),
        }

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def fallback_catch_all(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "status": "initialization_failed",
                "error": f"{type(exc).__name__}: {str(exc)}",
                "path": path_name,
                "traceback": traceback.format_exc(),
            },
        )
