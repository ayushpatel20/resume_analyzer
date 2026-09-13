from __future__ import annotations
import json
from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["Job Roles & Samples"])


@router.get("/job-roles")
def get_job_roles():
    """Retrieve list of pre-configured target job roles with required/preferred skills."""
    roles_file = settings.DATA_DIR / "job_roles.json"
    if roles_file.exists():
        with open(roles_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


@router.get("/sample-jds")
def get_sample_job_descriptions():
    """Retrieve preloaded realistic job descriptions for demonstration and testing."""
    samples_file = settings.DATA_DIR / "sample_job_descriptions.json"
    if samples_file.exists():
        with open(samples_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
