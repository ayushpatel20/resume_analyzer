from __future__ import annotations
class SuggestionEngine:
    """Generates ethical, actionable resume improvement suggestions based on detected gaps."""

    def generate_suggestions(
        self,
        detected_sections: dict[str, bool],
        extracted_info: dict,
        missing_job_skills: list[str],
        metrics_count: int,
        skills_count: int,
    ) -> list[dict]:
        """
        Produce categorized suggestions.
        Returns list of dicts: [{"category": str, "suggestion": str}]
        """
        suggestions = []

        # 1. Summary / Objective
        if not detected_sections.get("Summary") and not detected_sections.get("Objective"):
            suggestions.append({
                "category": "Structure",
                "suggestion": "Consider adding a concise 2-3 sentence professional summary highlighting your core strengths, career focus, and major achievements.",
            })

        # 2. LinkedIn Profile
        if extracted_info.get("linkedin") == "Not detected":
            suggestions.append({
                "category": "Contact & Links",
                "suggestion": "Consider adding your LinkedIn profile URL so recruiters can easily review your network and professional endorsements.",
            })

        # 3. GitHub / Portfolio Link
        if extracted_info.get("github") == "Not detected":
            suggestions.append({
                "category": "Contact & Links",
                "suggestion": "Consider adding your GitHub or technical portfolio link to showcase repositories, code samples, and open-source contributions.",
            })

        # 4. Projects Section
        if not detected_sections.get("Projects"):
            suggestions.append({
                "category": "Experience & Projects",
                "suggestion": "Consider adding 2–3 relevant technical projects with brief problem descriptions, technologies used, and your individual contributions.",
            })

        # 5. Work Experience / Internships
        if not detected_sections.get("Experience"):
            suggestions.append({
                "category": "Experience & Projects",
                "suggestion": "If you have completed any internships, part-time technical work, or open-source roles, consider listing them under an Experience section.",
            })

        # 6. Certifications
        if not detected_sections.get("Certifications"):
            suggestions.append({
                "category": "Credentials",
                "suggestion": "Consider listing relevant industry certifications (e.g. AWS, Oracle, Google Cloud, Coursera specializations) if applicable.",
            })

        # 7. Quantifiable Metrics & Action Verbs
        if metrics_count < 2:
            suggestions.append({
                "category": "Impact & Writing",
                "suggestion": "Consider adding measurable results (e.g., 'improved query performance by 30%', 'handled 5,000+ daily requests') to substantiate your accomplishments.",
            })

        # 8. Skill Gaps from Target Job Description (Ethical recommendation)
        if missing_job_skills:
            top_missing = missing_job_skills[:4]
            skills_str = ", ".join(top_missing)
            suggestions.append({
                "category": "Job Match",
                "suggestion": f"The job description explicitly prioritizes: {skills_str}. Consider highlighting relevant coursework, projects, or experience with these technologies if you genuinely possess them.",
            })

        # 9. Low overall skills detected
        if skills_count < 5:
            suggestions.append({
                "category": "Skills",
                "suggestion": "A dedicated 'Technical Skills' section categorized into Languages, Frameworks, and Developer Tools helps ATS scanners parse your proficiencies more effectively.",
            })

        return suggestions


suggestion_engine = SuggestionEngine()
