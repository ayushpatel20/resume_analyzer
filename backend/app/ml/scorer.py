from __future__ import annotations
import re
from app.config import settings


class ResumeScorer:
    """Calculates an independent 0-100 Resume Quality Score based on structured sections and depth."""

    def calculate_score(
        self,
        resume_text: str,
        detected_sections: dict[str, bool],
        extracted_info: dict,
        detected_skills: list[str],
    ) -> dict:
        """
        Evaluate resume quality against a comprehensive rubric.
        Returns:
            {
                "resume_score": float,
                "breakdown": dict[str, dict],
                "details": dict
            }
        """
        breakdown = {}

        # 1. Contact Info (Max: settings.SCORE_CONTACT = 10)
        contact_points = 0
        if extracted_info.get("email") != "Not detected":
            contact_points += 3
        if extracted_info.get("phone") != "Not detected":
            contact_points += 3
        if extracted_info.get("linkedin") != "Not detected":
            contact_points += 2
        if extracted_info.get("github") != "Not detected":
            contact_points += 2
        contact_score = min(settings.SCORE_CONTACT, contact_points)
        breakdown["Contact Information"] = {
            "score": contact_score,
            "max": settings.SCORE_CONTACT,
            "status": "Good" if contact_score >= 8 else "Needs Improvement",
        }

        # 2. Professional Summary or Objective (Max: 10)
        has_summary = detected_sections.get("Summary", False) or detected_sections.get("Objective", False)
        summary_score = settings.SCORE_SUMMARY if has_summary else 0
        breakdown["Summary / Objective"] = {
            "score": summary_score,
            "max": settings.SCORE_SUMMARY,
            "status": "Present" if has_summary else "Missing",
        }

        # 3. Education (Max: 10)
        has_education = detected_sections.get("Education", False)
        has_degree = extracted_info.get("degree") != "Not detected"
        edu_score = 0
        if has_education:
            edu_score += 6
        if has_degree:
            edu_score += 4
        edu_score = min(settings.SCORE_EDUCATION, edu_score)
        breakdown["Education"] = {
            "score": edu_score,
            "max": settings.SCORE_EDUCATION,
            "status": "Good" if edu_score >= 8 else ("Basic" if edu_score > 0 else "Missing"),
        }

        # 4. Skills Section & Quantity (Max: 15)
        has_skills_section = detected_sections.get("Skills", False)
        skills_count = len(detected_skills)
        skill_points = 0
        if has_skills_section:
            skill_points += 5
        if skills_count >= 10:
            skill_points += 10
        elif skills_count >= 5:
            skill_points += 6
        elif skills_count >= 2:
            skill_points += 3
        skill_score = min(settings.SCORE_SKILLS, skill_points)
        breakdown["Skills Section"] = {
            "score": skill_score,
            "max": settings.SCORE_SKILLS,
            "status": f"{skills_count} skills detected",
        }

        # 5. Projects Section (Max: 15)
        has_projects = detected_sections.get("Projects", False)
        project_score = 0
        if has_projects:
            project_score += 10
            # Check for multiple project indicators or tech stack mentions in projects
            if re.search(r"(?:github\.com|demo|deployed|built|designed|implemented)", resume_text, re.IGNORECASE):
                project_score += 5
        project_score = min(settings.SCORE_PROJECTS, project_score)
        breakdown["Projects"] = {
            "score": project_score,
            "max": settings.SCORE_PROJECTS,
            "status": "Well-documented" if project_score >= 12 else ("Present" if project_score > 0 else "Missing"),
        }

        # 6. Experience / Internship Section (Max: 15)
        has_exp = detected_sections.get("Experience", False)
        exp_score = settings.SCORE_EXPERIENCE if has_exp else 0
        breakdown["Work Experience / Internships"] = {
            "score": exp_score,
            "max": settings.SCORE_EXPERIENCE,
            "status": "Present" if has_exp else "Missing",
        }

        # 7. Certifications (Max: 10)
        has_cert = detected_sections.get("Certifications", False)
        cert_score = settings.SCORE_CERTIFICATIONS if has_cert else 0
        breakdown["Certifications"] = {
            "score": cert_score,
            "max": settings.SCORE_CERTIFICATIONS,
            "status": "Present" if has_cert else "Missing",
        }

        # 8. Achievements / Awards (Max: 5)
        has_achieve = detected_sections.get("Achievements", False) or detected_sections.get("Publications", False)
        achieve_score = settings.SCORE_ACHIEVEMENTS if has_achieve else 0
        breakdown["Achievements & Awards"] = {
            "score": achieve_score,
            "max": settings.SCORE_ACHIEVEMENTS,
            "status": "Present" if has_achieve else "Missing",
        }

        # 9. Measurable Metrics & Action Verbs (Max: 10)
        metric_matches = len(re.findall(r"\b(?:\d+%(?:\s+increase|\s+growth)?|\$\d+|\d+\+|\bimproved\b|\bboosted\b|\breduced\b|\baccelerated\b)", resume_text, re.IGNORECASE))
        metric_score = 0
        if metric_matches >= 4:
            metric_score = 10
        elif metric_matches >= 2:
            metric_score = 6
        elif metric_matches >= 1:
            metric_score = 3
        breakdown["Quantifiable Impact"] = {
            "score": metric_score,
            "max": settings.SCORE_KEYWORDS,
            "status": f"{metric_matches} impact indicators found",
        }

        total_score = sum(cat["score"] for cat in breakdown.values())
        total_score = round(min(100.0, max(0.0, float(total_score))), 1)

        return {
            "resume_score": total_score,
            "breakdown": breakdown,
            "metrics_count": metric_matches,
        }


resume_scorer = ResumeScorer()
