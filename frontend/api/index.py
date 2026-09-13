import os
import sys
from pathlib import Path

# Add backend directory to sys.path
current_dir = Path(__file__).resolve().parent
parent_backend = current_dir.parent.parent / "backend"
alt_backend = current_dir.parent / "backend"

if parent_backend.exists():
    sys.path.insert(0, str(parent_backend))
    sys.path.insert(0, str(current_dir.parent.parent))
elif alt_backend.exists():
    sys.path.insert(0, str(alt_backend))
    sys.path.insert(0, str(current_dir.parent))

os.environ["VERCEL"] = "1"

from app.main import app
