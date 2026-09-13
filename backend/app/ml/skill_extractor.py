import json
import re
from pathlib import Path
from app.config import settings


class SkillExtractor:
    def __init__(self, skills_path: Path | None = None):
        self.skills_path = skills_path or (settings.DATA_DIR / "skills.json")
        self.categories_skills: dict[str, list[str]] = {}
        self.flat_skills: list[str] = []
        self._load_skills()

    def _load_skills(self):
        """Load skills from JSON database."""
        if not self.skills_path.exists():
            # Fallback default skills if file not found
            self.categories_skills = {
                "PROGRAMMING": ["Python", "Java", "C++", "JavaScript", "TypeScript"],
                "DATA SCIENCE": ["Pandas", "NumPy", "SQL", "Excel", "Statistics"],
                "AI/ML": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
                "WEB": ["HTML", "CSS", "React", "FastAPI", "REST API"],
                "CLOUD/DEVOPS": ["Docker", "Git", "AWS", "Linux"],
            }
        else:
            with open(self.skills_path, "r", encoding="utf-8") as f:
                self.categories_skills = json.load(f)

        # Build flat list and category lookup
        self.flat_skills = []
        self.skill_to_category = {}
        for category, skills in self.categories_skills.items():
            for skill in skills:
                self.flat_skills.append(skill)
                self.skill_to_category[skill.lower()] = category

        # Sort longer phrases first to prioritize multi-word matches (e.g., "Machine Learning" before "Learning")
        self.sorted_skills = sorted(self.flat_skills, key=lambda s: len(s), reverse=True)

    def extract_skills(self, text: str) -> dict:
        """
        Extract skills from raw text safely using regex patterns and word boundaries.
        Returns:
            {
                "all_skills": list[str],
                "by_category": dict[str, list[str]],
                "skill_details": list[dict]
            }
        """
        if not text:
            return {"all_skills": [], "by_category": {}, "skill_details": []}

        # Normalize text spacing but keep case for special matching
        clean_text = " " + text + " "
        detected_set = set()
        by_category = {cat: [] for cat in self.categories_skills}

        # Special symbol mapping for C++, C#, .NET, etc.
        special_regexes = {
            "c++": r"(?:^|[\s,;/()\[\]])(c\+\+)(?:[\s,;/()\[\].]|$)",
            "c#": r"(?:^|[\s,;/()\[\]])(c\#)(?:[\s,;/()\[\].]|$)",
            "c": r"(?:^|[\s,;/()\[\]])([Cc])(?:[\s,;/()\[\].]|$)",
            "r": r"(?:^|[\s,;/()\[\]])([Rr])(?:[\s,;/()\[\].]|$)",
            ".net": r"(?:^|[\s,;/()\[\]])(\.net)(?:[\s,;/()\[\].]|$)",
        }

        # 1. Check special single-character or symbolic skills
        for skill_name in ["C++", "C#", "C", "R"]:
            lower_name = skill_name.lower()
            if lower_name in special_regexes:
                pattern = special_regexes[lower_name]
                if re.search(pattern, clean_text, re.IGNORECASE if len(skill_name) > 1 else 0):
                    # For single 'C' or 'R', verify it's under a technical context
                    if skill_name in ["C", "R"]:
                        context_check = re.search(
                            rf"(?:languages|skills|programming|c/c\+\+|r\/python|\b{skill_name}\b\s*(?:programming|language))",
                            clean_text,
                            re.IGNORECASE,
                        )
                        if context_check:
                            detected_set.add(skill_name)
                    else:
                        detected_set.add(skill_name)

        # 2. Match standard skills (case-insensitive with word boundary)
        for skill in self.sorted_skills:
            if skill in ["C", "C++", "C#", "R"]:
                continue  # Handled above

            escaped = re.escape(skill)
            # Use word boundaries
            pattern = rf"(?<!\w){escaped}(?!\w)"
            if re.search(pattern, clean_text, re.IGNORECASE):
                detected_set.add(skill)

        # Categorize detected skills
        detected_skills_list = sorted(list(detected_set))
        skill_details = []

        for skill in detected_skills_list:
            category = self.skill_to_category.get(skill.lower(), "OTHER")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(skill)
            skill_details.append({"name": skill, "category": category})

        # Prune empty categories
        by_category = {k: v for k, v in by_category.items() if v}

        return {
            "all_skills": detected_skills_list,
            "by_category": by_category,
            "skill_details": skill_details,
        }


skill_extractor = SkillExtractor()
