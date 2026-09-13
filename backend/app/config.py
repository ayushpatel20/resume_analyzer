import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure runtime directories exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer and Job Matching System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Security & JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "btech_ai_resume_analyzer_super_secret_key_2026_jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database: SQLite default for seamless local setup, PostgreSQL supported via env
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'resume_analyzer.db'}")

    # File Upload Limits
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: set = {".pdf"}

    # Scoring Weights (Configurable & Documented for Viva)
    # ATS Formula: 50% text/semantic similarity + 30% skill match + 20% keyword match
    WEIGHT_SEMANTIC_SIMILARITY: float = 0.50
    WEIGHT_SKILL_MATCH: float = 0.30
    WEIGHT_KEYWORD_MATCH: float = 0.20

    # Resume Quality Weights (Total: 100)
    SCORE_CONTACT: int = 10
    SCORE_SUMMARY: int = 10
    SCORE_EDUCATION: int = 10
    SCORE_SKILLS: int = 15
    SCORE_PROJECTS: int = 15
    SCORE_EXPERIENCE: int = 15
    SCORE_CERTIFICATIONS: int = 10
    SCORE_ACHIEVEMENTS: int = 5
    SCORE_KEYWORDS: int = 10

    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = DATA_DIR
    UPLOADS_DIR: Path = UPLOADS_DIR
    REPORTS_DIR: Path = REPORTS_DIR

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


settings = Settings()
