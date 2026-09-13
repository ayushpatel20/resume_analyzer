import re


class InfoExtractor:
    """Extracts candidate contact details, links, and degree information without hallucination."""

    EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_PATTERN = r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{4,5}|\+?\d{10,12})"
    LINKEDIN_PATTERN = r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+"
    GITHUB_PATTERN = r"(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+"

    DEGREE_PATTERNS = [
        r"\b(?:b\.?tech|bachelor\s+of\s+technology|b\.?e\.?|bachelor\s+of\s+engineering)\b",
        r"\b(?:m\.?tech|master\s+of\s+technology|m\.?e\.?|master\s+of\s+engineering)\b",
        r"\b(?:b\.?s\.?|bachelor\s+of\s+science|b\.?sc\.?)\b",
        r"\b(?:m\.?s\.?|master\s+of\s+science|m\.?sc\.?)\b",
        r"\b(?:bca|bachelor\s+of\s+computer\s+applications)\b",
        r"\b(?:mca|master\s+of\s+computer\s+applications)\b",
        r"\b(?:ph\.?d\.?|doctor\s+of\s+philosophy)\b",
        r"\b(?:bba|mba|bachelor\s+of\s+business\s+administration|master\s+of\s+business\s+administration)\b",
    ]

    def extract_name(self, text: str) -> str:
        """
        Extract candidate name from top lines using heuristic analysis.
        Avoids labels, emails, and urls.
        """
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines[:6]:  # Look within the top 6 lines
            # Skip if it contains email, url, phone, or heading keywords
            if "@" in line or "http" in line or "github" in line or "linkedin" in line:
                continue
            if re.search(r"(?:resume|curriculum|vitae|profile|summary|contact|phone)", line, re.IGNORECASE):
                continue
            # Remove bullets or extra chars
            clean_line = re.sub(r"[^a-zA-Z\s\.]", "", line).strip()
            words = clean_line.split()
            # Most candidate names have 2 to 4 words, each capitalized
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                return clean_line

        return "Not detected"

    def extract_email(self, text: str) -> str:
        match = re.search(self.EMAIL_PATTERN, text)
        return match.group(0) if match else "Not detected"

    def extract_phone(self, text: str) -> str:
        # Match +91 98765 43210, (555) 123-4567, +1-555-123-4567, 9876543210
        pattern = r"(?:\+?\d{1,3}[-.\s]*)?(?:\(?\d{2,5}\)?[-.\s]*)?\d{3,5}[-.\s]*\d{4,5}"
        for match in re.finditer(pattern, text):
            candidate = match.group(0).strip()
            digits = re.sub(r"\D", "", candidate)
            if 10 <= len(digits) <= 15:
                return candidate
        return "Not detected"

    def extract_linkedin(self, text: str) -> str:
        match = re.search(self.LINKEDIN_PATTERN, text, re.IGNORECASE)
        if match:
            url = match.group(0)
            return url if url.startswith("http") else f"https://{url}"
        if "linkedin.com" in text.lower():
            # Loose match
            loose = re.search(r"linkedin\.com\/[^\s,]+", text, re.IGNORECASE)
            if loose:
                return f"https://{loose.group(0)}"
        return "Not detected"

    def extract_github(self, text: str) -> str:
        match = re.search(self.GITHUB_PATTERN, text, re.IGNORECASE)
        if match:
            url = match.group(0)
            return url if url.startswith("http") else f"https://{url}"
        if "github.com" in text.lower():
            loose = re.search(r"github\.com\/[^\s,]+", text, re.IGNORECASE)
            if loose:
                return f"https://{loose.group(0)}"
        return "Not detected"

    def extract_degree(self, text: str) -> str:
        for pattern in self.DEGREE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                matched_str = match.group(0).strip()
                # Format common degree acronyms nicely
                lower = matched_str.lower()
                if "b.tech" in lower or "btech" in lower or "bachelor of technology" in lower:
                    return "B.Tech (Bachelor of Technology)"
                if "m.tech" in lower or "mtech" in lower or "master of technology" in lower:
                    return "M.Tech (Master of Technology)"
                if "b.e" in lower or "be" in lower or "bachelor of engineering" in lower:
                    return "B.E. (Bachelor of Engineering)"
                if "b.sc" in lower or "bsc" in lower or "bachelor of science" in lower:
                    return "B.Sc (Bachelor of Science)"
                if "mca" in lower or "master of computer applications" in lower:
                    return "MCA (Master of Computer Applications)"
                if "bca" in lower:
                    return "BCA (Bachelor of Computer Applications)"
                return matched_str.title()
        return "Not detected"

    def extract_info(self, text: str) -> dict:
        """Extract all identifiable information from resume text."""
        return {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "linkedin": self.extract_linkedin(text),
            "github": self.extract_github(text),
            "degree": self.extract_degree(text),
        }


info_extractor = InfoExtractor()
