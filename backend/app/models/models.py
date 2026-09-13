import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    extracted_text = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resumes")
    analyses = relationship("Analysis", back_populates="resume", cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)

    job_title = Column(String(200), default="Target Job")
    job_description = Column(Text, nullable=False)

    # Scores (0 to 100)
    ats_score = Column(Float, nullable=False)
    resume_score = Column(Float, nullable=False)
    skill_match_score = Column(Float, nullable=False)
    keyword_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)

    # JSON snapshots for fast retrieval of rich UI details
    extracted_info = Column(JSON, nullable=True)  # Name, email, phone, links, education
    detected_sections = Column(JSON, nullable=True)  # Present/missing sections
    score_breakdown = Column(JSON, nullable=True)  # Breakdown components

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    skills = relationship("AnalysisSkill", back_populates="analysis", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="analysis", cascade="all, delete-orphan")
    suggestions = relationship("Suggestion", back_populates="analysis", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)


class AnalysisSkill(Base):
    __tablename__ = "analysis_skills"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # "matched", "missing", "detected"

    # Relationship
    analysis = relationship("Analysis", back_populates="skills")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False)
    job_role = Column(String(150), nullable=False)
    score = Column(Float, nullable=False)
    matched_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)

    # Relationship
    analysis = relationship("Analysis", back_populates="recommendations")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), default="General")
    suggestion = Column(Text, nullable=False)

    # Relationship
    analysis = relationship("Analysis", back_populates="suggestions")
