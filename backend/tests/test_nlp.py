from app.ml.skill_extractor import skill_extractor
from app.ml.section_parser import section_parser
from app.ml.info_extractor import info_extractor
from app.ml.matcher import ats_matcher
from app.ml.scorer import resume_scorer
from app.ml.recommender import job_recommender


def test_skill_extraction():
    text = (
        "Experienced software developer skilled in Python, SQL, Docker, Machine Learning, "
        "and FastAPI. Strong background in Pandas and Git."
    )
    result = skill_extractor.extract_skills(text)
    detected = result["all_skills"]

    assert "Python" in detected
    assert "SQL" in detected
    assert "Docker" in detected
    assert "Machine Learning" in detected
    assert "FastAPI" in detected
    assert "Pandas" in detected
    assert "Git" in detected


def test_special_skill_c_plus_plus():
    text = "Proficient in C++, Python, and C# programming."
    result = skill_extractor.extract_skills(text)
    detected = result["all_skills"]

    assert "C++" in detected
    assert "C#" in detected


def test_section_parsing():
    text = """
    John Doe
    PROFESSIONAL SUMMARY
    Dedicated software engineer with 3 years of experience.
    
    EDUCATION
    B.Tech Computer Science, 2024
    
    TECHNICAL SKILLS
    Python, SQL, React
    
    PROJECTS
    Built an AI Resume Analyzer.
    
    EXPERIENCE
    Software Engineer at TechCorp.
    """
    sections = section_parser.detect_sections(text)
    assert sections["Summary"] is True
    assert sections["Education"] is True
    assert sections["Skills"] is True
    assert sections["Projects"] is True
    assert sections["Experience"] is True


def test_info_extraction():
    text = """
    Rahul Verma
    Email: rahul.verma@example.com
    Phone: +91 98765 43210
    LinkedIn: https://linkedin.com/in/rahul-verma
    GitHub: https://github.com/rahul-verma
    Degree: B.Tech in Computer Science and Engineering
    """
    info = info_extractor.extract_info(text)
    assert info["email"] == "rahul.verma@example.com"
    assert info["phone"] == "+91 98765 43210"
    assert "linkedin.com/in/rahul-verma" in info["linkedin"]
    assert "github.com/rahul-verma" in info["github"]
    assert "B.Tech" in info["degree"]


def test_ats_matching():
    resume = "Experienced in Python, SQL, Pandas, NumPy, Scikit-learn, and Machine Learning."
    jd = "Looking for a Data Scientist with strong Python, SQL, Machine Learning, and Pandas expertise."

    match = ats_matcher.match(resume, jd)
    assert match["ats_score"] > 50.0
    assert "Python" in match["matched_skills"]
    assert "SQL" in match["matched_skills"]
    assert "Machine Learning" in match["matched_skills"]
    assert len(match["missing_skills"]) == 0


def test_job_recommendation():
    skills = ["Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning", "SQL", "Statistics"]
    recs = job_recommender.recommend_roles(skills)
    assert len(recs) > 0
    top_role = recs[0]["job_role"]
    # Should recommend Data Scientist or Machine Learning Engineer or Data Analyst
    assert top_role in ["Data Scientist", "Machine Learning Engineer", "Data Analyst"]
