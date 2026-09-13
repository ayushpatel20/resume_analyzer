from __future__ import annotations
import datetime
from typing import Any
from pydantic import BaseModel, Field, ConfigDict


class AnalysisCreate(BaseModel):
    resume_id: int | None = None
    job_title: str = Field(default="Target Job", max_length=200)
    job_description: str = Field(..., min_length=10)


class AnalysisSkillOut(BaseModel):
    id: int
    skill_name: str
    category: str
    status: str  # "matched", "missing", "detected"

    model_config = ConfigDict(from_attributes=True)


class RecommendationOut(BaseModel):
    id: int
    job_role: str
    score: float
    matched_skills: list[str]
    missing_skills: list[str]

    model_config = ConfigDict(from_attributes=True)


class SuggestionOut(BaseModel):
    id: int
    category: str
    suggestion: str

    model_config = ConfigDict(from_attributes=True)


class AnalysisSummaryOut(BaseModel):
    id: int
    user_id: int
    resume_id: int
    resume_filename: str = ""
    job_title: str
    ats_score: float
    resume_score: float
    skill_match_score: float
    keyword_score: float
    semantic_score: float
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisDetailOut(AnalysisSummaryOut):
    job_description: str
    extracted_info: dict[str, Any] | None = None
    detected_sections: dict[str, bool] | None = None
    score_breakdown: dict[str, Any] | None = None
    skills: list[AnalysisSkillOut] = []
    recommendations: list[RecommendationOut] = []
    suggestions: list[SuggestionOut] = []


class DashboardStatsOut(BaseModel):
    total_resumes: int
    total_analyses: int
    latest_ats_score: float | None = None
    latest_resume_score: float | None = None
    total_skills_detected: int = 0
    total_missing_skills: int = 0
    recent_analyses: list[AnalysisSummaryOut] = []
