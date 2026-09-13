from __future__ import annotations
import datetime
from pydantic import BaseModel, ConfigDict


class ResumeBase(BaseModel):
    filename: str
    file_size: int


class ResumeOut(ResumeBase):
    id: int
    user_id: int
    uploaded_at: datetime.datetime
    analysis_count: int = 0
    latest_ats_score: float | None = None
    latest_resume_score: float | None = None

    model_config = ConfigDict(from_attributes=True)


class ResumeDetail(ResumeOut):
    extracted_text: str
    file_path: str
