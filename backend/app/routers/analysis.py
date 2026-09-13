from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import (
    User,
    Resume,
    Analysis,
    AnalysisSkill,
    Recommendation,
    Suggestion,
)
from app.schemas.analysis import (
    AnalysisDetailOut,
    AnalysisSummaryOut,
    DashboardStatsOut,
    AnalysisSkillOut,
    RecommendationOut,
    SuggestionOut,
)
from app.auth.deps import get_current_user

router = APIRouter(prefix="/analysis", tags=["Analysis"])


def _get_ml_services():
    """Lazily import and return ML and PDF processing services to ensure fast, safe serverless startup."""
    from app.services.pdf_service import pdf_service
    from app.ml.info_extractor import info_extractor
    from app.ml.section_parser import section_parser
    from app.ml.matcher import ats_matcher
    from app.ml.scorer import resume_scorer
    from app.ml.recommender import job_recommender
    from app.ml.suggestion_engine import suggestion_engine

    return (
        pdf_service,
        info_extractor,
        section_parser,
        ats_matcher,
        resume_scorer,
        job_recommender,
        suggestion_engine,
    )



def _build_analysis_detail(analysis: Analysis) -> AnalysisDetailOut:
    """Helper to convert ORM Analysis into AnalysisDetailOut schema."""
    skills_out = [
        AnalysisSkillOut(
            id=s.id,
            skill_name=s.skill_name,
            category=s.category,
            status=s.status,
        )
        for s in analysis.skills
    ]
    recs_out = [
        RecommendationOut(
            id=r.id,
            job_role=r.job_role,
            score=r.score,
            matched_skills=r.matched_skills or [],
            missing_skills=r.missing_skills or [],
        )
        for r in analysis.recommendations
    ]
    suggs_out = [
        SuggestionOut(
            id=s.id,
            category=s.category,
            suggestion=s.suggestion,
        )
        for s in analysis.suggestions
    ]

    return AnalysisDetailOut(
        id=analysis.id,
        user_id=analysis.user_id,
        resume_id=analysis.resume_id,
        resume_filename=analysis.resume.filename if analysis.resume else "Uploaded Resume",
        job_title=analysis.job_title,
        job_description=analysis.job_description,
        ats_score=analysis.ats_score,
        resume_score=analysis.resume_score,
        skill_match_score=analysis.skill_match_score,
        keyword_score=analysis.keyword_score,
        semantic_score=analysis.semantic_score,
        extracted_info=analysis.extracted_info,
        detected_sections=analysis.detected_sections,
        score_breakdown=analysis.score_breakdown,
        skills=skills_out,
        recommendations=recs_out,
        suggestions=suggs_out,
        created_at=analysis.created_at,
    )


@router.post("/analyze", response_model=AnalysisDetailOut, status_code=status.HTTP_201_CREATED)
async def analyze_resume(
    resume_file: UploadFile | None = File(None),
    resume_id: int | None = Form(None),
    job_title: str = Form("Target Job"),
    job_description: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Perform full end-to-end resume analysis and ATS job matching.
    Accepts either an uploaded PDF file or an existing resume_id, plus the job description text.
    """
    if len(job_description.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description must be at least 10 characters long.",
        )

    # 0. Lazy-load ML services
    (
        pdf_service,
        info_extractor,
        section_parser,
        ats_matcher,
        resume_scorer,
        job_recommender,
        suggestion_engine,
    ) = _get_ml_services()

    # 1. Resolve resume record and extracted text
    resume: Resume | None = None
    if resume_file:
        saved_path, original_filename, file_size = pdf_service.validate_and_save(resume_file)

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
    elif resume_id:
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified resume not found.")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either a PDF resume file or an existing resume_id must be provided.",
        )

    resume_text = resume.extracted_text

    # 2. Extract Candidate Information
    extracted_info = info_extractor.extract_info(resume_text)

    # 3. Detect Resume Sections
    detected_sections = section_parser.detect_sections(resume_text)

    # 4. ATS & Skill Matching (TF-IDF + Cosine Sim + Skills + Keywords)
    match_result = ats_matcher.match(resume_text, job_description)

    # 5. Calculate Resume Quality Score (0-100 rubric)
    scorer_result = resume_scorer.calculate_score(
        resume_text=resume_text,
        detected_sections=detected_sections,
        extracted_info=extracted_info,
        detected_skills=match_result["resume_skills"],
    )

    # 6. Job Role Recommendations
    top_recommendations = job_recommender.recommend_roles(
        candidate_skills=match_result["resume_skills"],
        top_n=5,
    )

    # 7. Resume Improvement Suggestions
    suggestions_list = suggestion_engine.generate_suggestions(
        detected_sections=detected_sections,
        extracted_info=extracted_info,
        missing_job_skills=match_result["missing_skills"],
        metrics_count=scorer_result["metrics_count"],
        skills_count=len(match_result["resume_skills"]),
    )

    # 8. Persist Analysis Record
    score_breakdown = {
        "ats_formula": match_result["score_breakdown"],
        "resume_rubric": scorer_result["breakdown"],
        "keywords_matched": match_result["matched_keywords"],
        "keywords_missing": match_result["missing_keywords"],
    }

    clean_title = job_title.strip() if job_title and job_title.strip() else "Target Job"

    analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_title=clean_title,
        job_description=job_description.strip(),
        ats_score=match_result["ats_score"],
        resume_score=scorer_result["resume_score"],
        skill_match_score=match_result["skill_match_score"],
        keyword_score=match_result["keyword_score"],
        semantic_score=match_result["semantic_score"],
        extracted_info=extracted_info,
        detected_sections=detected_sections,
        score_breakdown=score_breakdown,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # 9. Persist Matched and Missing Skills
    for skill_name in match_result["matched_skills"]:
        category = ats_matcher.skill_to_cat.get(skill_name.lower(), "OTHER") if hasattr(ats_matcher, "skill_to_cat") else "Skill"
        db.add(AnalysisSkill(
            analysis_id=analysis.id,
            skill_name=skill_name,
            category="Matched",
            status="matched",
        ))

    for skill_name in match_result["missing_skills"]:
        db.add(AnalysisSkill(
            analysis_id=analysis.id,
            skill_name=skill_name,
            category="Missing",
            status="missing",
        ))

    # Also record skills detected in resume that were not in JD
    resume_only_skills = set(match_result["resume_skills"]) - set(match_result["matched_skills"])
    for skill_name in resume_only_skills:
        db.add(AnalysisSkill(
            analysis_id=analysis.id,
            skill_name=skill_name,
            category="Detected",
            status="detected",
        ))

    # 10. Persist Recommendations
    for rec in top_recommendations:
        db.add(Recommendation(
            analysis_id=analysis.id,
            job_role=rec["job_role"],
            score=rec["score"],
            matched_skills=rec["matched_skills"],
            missing_skills=rec["missing_skills"],
        ))

    # 11. Persist Suggestions
    for sugg in suggestions_list:
        db.add(Suggestion(
            analysis_id=analysis.id,
            category=sugg["category"],
            suggestion=sugg["suggestion"],
        ))

    db.commit()
    db.refresh(analysis)

    return _build_analysis_detail(analysis)


@router.get("", response_model=list[AnalysisSummaryOut])
def get_user_analyses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve all analysis records for the authenticated user, ordered from newest to oldest."""
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).all()
    results = []
    for a in analyses:
        results.append(
            AnalysisSummaryOut(
                id=a.id,
                user_id=a.user_id,
                resume_id=a.resume_id,
                resume_filename=a.resume.filename if a.resume else "Uploaded Resume",
                job_title=a.job_title,
                ats_score=a.ats_score,
                resume_score=a.resume_score,
                skill_match_score=a.skill_match_score,
                keyword_score=a.keyword_score,
                semantic_score=a.semantic_score,
                created_at=a.created_at,
            )
        )
    return results


@router.get("/dashboard-stats", response_model=DashboardStatsOut)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return aggregated KPI metrics and recent analyses for the user dashboard."""
    total_resumes = db.query(Resume).filter(Resume.user_id == current_user.id).count()
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).all()

    total_analyses = len(analyses)
    latest = analyses[0] if analyses else None

    # Count skills from latest analysis
    detected_count = 0
    missing_count = 0
    if latest:
        detected_count = db.query(AnalysisSkill).filter(
            AnalysisSkill.analysis_id == latest.id,
            AnalysisSkill.status.in_(["matched", "detected"]),
        ).count()
        missing_count = db.query(AnalysisSkill).filter(
            AnalysisSkill.analysis_id == latest.id,
            AnalysisSkill.status == "missing",
        ).count()

    recent_summaries = [
        AnalysisSummaryOut(
            id=a.id,
            user_id=a.user_id,
            resume_id=a.resume_id,
            resume_filename=a.resume.filename if a.resume else "Uploaded Resume",
            job_title=a.job_title,
            ats_score=a.ats_score,
            resume_score=a.resume_score,
            skill_match_score=a.skill_match_score,
            keyword_score=a.keyword_score,
            semantic_score=a.semantic_score,
            created_at=a.created_at,
        )
        for a in analyses[:5]
    ]

    return DashboardStatsOut(
        total_resumes=total_resumes,
        total_analyses=total_analyses,
        latest_ats_score=latest.ats_score if latest else None,
        latest_resume_score=latest.resume_score if latest else None,
        total_skills_detected=detected_count,
        total_missing_skills=missing_count,
        recent_analyses=recent_summaries,
    )


@router.get("/{analysis_id}", response_model=AnalysisDetailOut)
def get_analysis_detail(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve the full analysis result by ID."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")

    return _build_analysis_detail(analysis)


@router.delete("/{analysis_id}", status_code=status.HTTP_200_OK)
def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a specific analysis record."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")

    db.delete(analysis)
    db.commit()
    return {"message": "Analysis deleted successfully."}


@router.delete("/clear-history", status_code=status.HTTP_200_OK)
def clear_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete all analysis records for the current user."""
    db.query(Analysis).filter(Analysis.user_id == current_user.id).delete()
    db.commit()
    return {"message": "All analysis history has been cleared."}
