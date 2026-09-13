from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Analysis
from app.auth.deps import get_current_user
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/{analysis_id}")
def download_analysis_report(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate and return a downloadable PDF evaluation report for a given analysis record."""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis record not found.",
        )

    # Prepare data dictionary for report service
    analysis_data = {
        "id": analysis.id,
        "job_title": analysis.job_title,
        "ats_score": analysis.ats_score,
        "resume_score": analysis.resume_score,
        "skill_match_score": analysis.skill_match_score,
        "keyword_score": analysis.keyword_score,
        "semantic_score": analysis.semantic_score,
        "extracted_info": analysis.extracted_info or {},
        "detected_sections": analysis.detected_sections or {},
        "created_at": analysis.created_at,
        "skills": analysis.skills,
        "recommendations": analysis.recommendations,
        "suggestions": analysis.suggestions,
    }

    try:
        report_path = report_service.generate_pdf_report(analysis_data)
        return FileResponse(
            path=str(report_path),
            filename=report_path.name,
            media_type="application/pdf",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compile PDF report: {str(e)}",
        )
