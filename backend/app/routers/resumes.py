import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Resume, Analysis
from app.schemas.resume import ResumeOut, ResumeDetail
from app.auth.deps import get_current_user
from app.services.pdf_service import pdf_service

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeDetail, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a PDF resume, validate its contents, extract text, and save record."""
    saved_path, original_filename, file_size = pdf_service.validate_and_save(file)
    extracted_text = pdf_service.extract_text(saved_path)

    resume = Resume(
        user_id=current_user.id,
        filename=original_filename,
        file_path=str(saved_path),
        file_size=file_size,
        extracted_text=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeDetail(
        id=resume.id,
        user_id=resume.user_id,
        filename=resume.filename,
        file_path=resume.file_path,
        file_size=resume.file_size,
        extracted_text=resume.extracted_text,
        uploaded_at=resume.uploaded_at,
        analysis_count=0,
        latest_ats_score=None,
        latest_resume_score=None,
    )


@router.get("", response_model=list[ResumeOut])
def get_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all resumes uploaded by the current user."""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc()).all()
    results = []
    for r in resumes:
        analyses = db.query(Analysis).filter(Analysis.resume_id == r.id).order_by(Analysis.created_at.desc()).all()
        latest = analyses[0] if analyses else None
        results.append(
            ResumeOut(
                id=r.id,
                user_id=r.user_id,
                filename=r.filename,
                file_size=r.file_size,
                uploaded_at=r.uploaded_at,
                analysis_count=len(analyses),
                latest_ats_score=latest.ats_score if latest else None,
                latest_resume_score=latest.resume_score if latest else None,
            )
        )
    return results


@router.get("/{resume_id}", response_model=ResumeDetail)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve details and extracted text of a specific resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    analyses = db.query(Analysis).filter(Analysis.resume_id == resume.id).order_by(Analysis.created_at.desc()).all()
    latest = analyses[0] if analyses else None

    return ResumeDetail(
        id=resume.id,
        user_id=resume.user_id,
        filename=resume.filename,
        file_path=resume.file_path,
        file_size=resume.file_size,
        extracted_text=resume.extracted_text,
        uploaded_at=resume.uploaded_at,
        analysis_count=len(analyses),
        latest_ats_score=latest.ats_score if latest else None,
        latest_resume_score=latest.resume_score if latest else None,
    )


@router.delete("/{resume_id}", status_code=status.HTTP_200_OK)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a resume and its stored file."""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    # Remove physical file if it exists
    try:
        file_p = Path(resume.file_path)
        if file_p.exists():
            file_p.unlink()
    except Exception:
        pass

    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted successfully"}
