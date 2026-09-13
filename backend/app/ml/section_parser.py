import re


class SectionParser:
    """Detects resume sections using robust heading pattern matching."""

    SECTION_PATTERNS = {
        "Summary": [
            r"\b(professional\s+summary|summary|profile|about\s+me|career\s+summary|personal\s+statement)\b",
        ],
        "Objective": [
            r"\b(career\s+objective|objective|professional\s+objective)\b",
        ],
        "Education": [
            r"\b(education|academic\s+background|academic\s+qualifications|qualification|qualifications|degrees)\b",
        ],
        "Skills": [
            r"\b(skills|technical\s+skills|core\s+competencies|key\s+skills|expertise|technologies|proficiencies)\b",
        ],
        "Experience": [
            r"\b(work\s+experience|professional\s+experience|experience|employment\s+history|internships?|work\s+history)\b",
        ],
        "Projects": [
            r"\b(projects|academic\s+projects|personal\s+projects|key\s+projects|technical\s+projects)\b",
        ],
        "Certifications": [
            r"\b(certifications?|certificates?|licenses?|credentials?|accreditations?)\b",
        ],
        "Achievements": [
            r"\b(achievements|awards|honors|accolades|recognitions?)\b",
        ],
        "Publications": [
            r"\b(publications|research\s+papers?|conferences?|patents?)\b",
        ],
        "Contact": [
            r"\b(contact|contact\s+information|personal\s+details)\b",
        ],
    }

    def detect_sections(self, text: str) -> dict[str, bool]:
        """
        Check presence of key resume sections.
        Returns dict like: {"Education": True, "Projects": True, "Summary": False, ...}
        """
        if not text:
            return {sec: False for sec in self.SECTION_PATTERNS}

        results = {}
        lines = text.splitlines()

        for section, patterns in self.SECTION_PATTERNS.items():
            detected = False

            # Check if any line looks like a header matching the section
            for pattern in patterns:
                # 1. Line-level check for headers (e.g. standalone heading "EDUCATION" or "## Education")
                for line in lines[:80]:  # check headers
                    clean_line = line.strip().rstrip(":")
                    if len(clean_line) <= 40 and re.search(pattern, clean_line, re.IGNORECASE):
                        detected = True
                        break

                if detected:
                    break

                # 2. General regex search if heading wasn't isolated
                if re.search(pattern, text, re.IGNORECASE):
                    detected = True
                    break

            results[section] = detected

        # If email or phone is found anywhere in the resume, Contact is considered present
        if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text):
            results["Contact"] = True

        return results


section_parser = SectionParser()
