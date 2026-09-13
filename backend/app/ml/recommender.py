import json
from pathlib import Path
from app.config import settings


class JobRecommender:
    """Matches candidate skills with curated job profiles to recommend top roles."""

    def __init__(self, roles_path: Path | None = None):
        self.roles_path = roles_path or (settings.DATA_DIR / "job_roles.json")
        self.roles_data: dict[str, dict] = {}
        self._load_roles()

    def _load_roles(self):
        if not self.roles_path.exists():
            self.roles_data = {}
            return
        with open(self.roles_path, "r", encoding="utf-8") as f:
            self.roles_data = json.load(f)

    def recommend_roles(self, candidate_skills: list[str], top_n: int = 5) -> list[dict]:
        """
        Rank job roles based on candidate skill coverage.
        Returns sorted list of top_n roles with match score and skill breakdown.
        """
        if not self.roles_data:
            return []

        candidate_set = {s.lower() for s in candidate_skills}
        recommendations = []

        for role_name, role_info in self.roles_data.items():
            req_skills = role_info.get("required_skills", [])
            pref_skills = role_info.get("preferred_skills", [])

            # Matched & Missing for required
            matched_req = [s for s in req_skills if s.lower() in candidate_set]
            missing_req = [s for s in req_skills if s.lower() not in candidate_set]

            # Matched & Missing for preferred
            matched_pref = [s for s in pref_skills if s.lower() in candidate_set]
            missing_pref = [s for s in pref_skills if s.lower() not in candidate_set]

            # Weighted scoring: Required skills have 2x weight of preferred skills
            req_weight = 2.0
            pref_weight = 1.0

            total_possible = (len(req_skills) * req_weight) + (len(pref_skills) * pref_weight)
            total_earned = (len(matched_req) * req_weight) + (len(matched_pref) * pref_weight)

            if total_possible > 0:
                match_percentage = round((total_earned / total_possible) * 100, 1)
            else:
                match_percentage = 0.0

            recommendations.append({
                "job_role": role_name,
                "description": role_info.get("description", ""),
                "score": match_percentage,
                "matched_skills": matched_req + matched_pref,
                "missing_skills": missing_req + missing_pref,
                "matched_required_count": len(matched_req),
                "total_required_count": len(req_skills),
            })

        # Sort descending by match score
        recommendations.sort(key=lambda r: r["score"], reverse=True)
        return recommendations[:top_n]


job_recommender = JobRecommender()
