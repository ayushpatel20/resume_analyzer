from __future__ import annotations
import math
import re
from app.config import settings
from app.ml.skill_extractor import skill_extractor

# Optional scikit-learn import for local / high-performance setups
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class ATSMatcher:
    """
    Computes ATS-style compatibility score between Resume and Job Description using:
    1. TF-IDF vectorization + Cosine Similarity (Semantic / Text Similarity)
    2. Exact & Semantic Skill Match Ratio
    3. Keyword Coverage
    Formula:
      ATS Score = (50% Semantic) + (30% Skill Match) + (20% Keyword Coverage)
    """

    STOP_WORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
        "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
        "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
        "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
        "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
        "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
        "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
        "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
        "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
        "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
        "they've", "this", "those", "through", "to", "too", "under", "until", "up",
        "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
        "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
        "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
        "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
        "yourself", "yourselves", "looking", "seeking", "requirements", "responsibilities",
        "experience", "years", "candidate", "role", "team", "work", "job", "company"
    }

    def _pure_python_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Pure-Python TF-IDF + Cosine Similarity algorithm for zero-dependency serverless environments."""
        def tokenize(text: str) -> list[str]:
            words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
            meaningful = [w for w in words if w not in self.STOP_WORDS]
            bigrams = [f"{meaningful[i]} {meaningful[i+1]}" for i in range(len(meaningful) - 1)]
            return meaningful + bigrams

        tokens1 = tokenize(text1)
        tokens2 = tokenize(text2)
        if not tokens1 or not tokens2:
            return 0.0

        set1 = set(tokens1)
        set2 = set(tokens2)
        vocab = set1 | set2
        N = 2

        tf1 = {t: tokens1.count(t) for t in set1}
        tf2 = {t: tokens2.count(t) for t in set2}

        vec1, vec2 = {}, {}
        for t in vocab:
            df = (1 if t in set1 else 0) + (1 if t in set2 else 0)
            idf = math.log((1 + N) / (1 + df)) + 1.0
            if t in tf1:
                vec1[t] = (1 + math.log(tf1[t])) * idf
            if t in tf2:
                vec2[t] = (1 + math.log(tf2[t])) * idf

        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0

        dot = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in vocab)
        return round(float(dot / (norm1 * norm2)) * 100, 1)

    def compute_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        """Compute TF-IDF Cosine Similarity between resume and job description."""
        if not resume_text or not jd_text:
            return 0.0

        if SKLEARN_AVAILABLE:
            try:
                vectorizer = TfidfVectorizer(
                    stop_words="english",
                    ngram_range=(1, 2),
                    max_features=2500,
                )
                tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                return round(float(similarity) * 100, 1)
            except Exception:
                pass

        # Robust pure-python TF-IDF cosine similarity fallback
        try:
            return self._pure_python_tfidf_similarity(resume_text, jd_text)
        except Exception:
            return 0.0


    def extract_keywords(self, text: str, max_keywords: int = 25) -> list[str]:
        """Extract top representative keywords from job description."""
        if not text:
            return []

        # Find words with 3+ characters
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        meaningful = [w for w in words if w not in self.STOP_WORDS]

        # Count frequencies
        freq: dict[str, int] = {}
        for w in meaningful:
            freq[w] = freq.get(w, 0) + 1

        # Sort by frequency
        sorted_keywords = sorted(freq.items(), key=lambda item: item[1], reverse=True)
        return [k for k, _ in sorted_keywords[:max_keywords]]

    def match(self, resume_text: str, jd_text: str) -> dict:
        """
        Execute full matching pipeline.
        Returns comprehensive scores, matched skills, missing skills, and keywords.
        """
        # 1. Extract skills from both texts
        resume_skill_data = skill_extractor.extract_skills(resume_text)
        jd_skill_data = skill_extractor.extract_skills(jd_text)

        resume_skills_set = set(resume_skill_data["all_skills"])
        jd_skills_set = set(jd_skill_data["all_skills"])

        # Matched & Missing skills
        matched_skills = sorted(list(resume_skills_set.intersection(jd_skills_set)))
        missing_skills = sorted(list(jd_skills_set - resume_skills_set))

        # Skill match score calculation
        if jd_skills_set:
            skill_match_score = round((len(matched_skills) / len(jd_skills_set)) * 100, 1)
        else:
            # If JD didn't explicitly mention tracked skills, base it on resume skills count
            skill_match_score = min(100.0, round(len(resume_skills_set) * 8.0, 1))

        # 2. Semantic text similarity (TF-IDF + Cosine Similarity)
        semantic_score = self.compute_semantic_similarity(resume_text, jd_text)

        # 3. Keyword analysis
        jd_keywords = self.extract_keywords(jd_text, max_keywords=20)
        resume_lower = resume_text.lower()
        matched_keywords = [kw for kw in jd_keywords if kw in resume_lower]
        missing_keywords = [kw for kw in jd_keywords if kw not in resume_lower]

        if jd_keywords:
            keyword_score = round((len(matched_keywords) / len(jd_keywords)) * 100, 1)
        else:
            keyword_score = 50.0

        # 4. Final ATS Score Formula
        w_sem = settings.WEIGHT_SEMANTIC_SIMILARITY
        w_skill = settings.WEIGHT_SKILL_MATCH
        w_kw = settings.WEIGHT_KEYWORD_MATCH

        ats_score = round(
            (w_sem * semantic_score) + (w_skill * skill_match_score) + (w_kw * keyword_score),
            1,
        )
        ats_score = max(0.0, min(100.0, ats_score))

        return {
            "ats_score": ats_score,
            "semantic_score": semantic_score,
            "skill_match_score": skill_match_score,
            "keyword_score": keyword_score,
            "resume_skills": resume_skill_data["all_skills"],
            "resume_skills_by_category": resume_skill_data["by_category"],
            "jd_skills": jd_skill_data["all_skills"],
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "total_jd_skills": len(jd_skills_set),
            "total_matched_skills": len(matched_skills),
            "total_missing_skills": len(missing_skills),
            "score_breakdown": {
                "formula": f"({int(w_sem*100)}% Semantic) + ({int(w_skill*100)}% Skills) + ({int(w_kw*100)}% Keywords)",
                "semantic_weight": w_sem,
                "skill_weight": w_skill,
                "keyword_weight": w_kw,
            },
        }


ats_matcher = ATSMatcher()
