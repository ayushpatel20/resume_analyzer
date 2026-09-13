import os
import sys
from pathlib import Path

# Add backend directory to sys.path so that 'app' can be imported seamlessly
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"

sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(root_dir))

# Ensure VERCEL environment flag is detected
os.environ["VERCEL"] = "1"

from app.main import app
