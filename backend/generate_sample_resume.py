from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PDF = BASE_DIR / "data" / "sample_resume.pdf"


def create_sample_resume():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=35,
        bottomMargin=35,
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "CandidateName",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        fontName="Helvetica-Bold",
        alignment=1,  # Center
    )
    contact_style = ParagraphStyle(
        "ContactLine",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569"),
        alignment=1,  # Center
    )
    section_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1e40af"),
        fontName="Helvetica-Bold",
        spaceBefore=8,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=2,
    )

    story = []

    # 1. Header
    story.append(Paragraph("Aarav Sharma", header_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "Email: aarav.sharma@example.com | Phone: +91 98765 43210 | Bangalore, India<br/>"
        "LinkedIn: https://linkedin.com/in/aarav-sharma-dev | GitHub: https://github.com/aarav-sharma",
        contact_style,
    ))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=6))

    # 2. Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
    story.append(Paragraph(
        "Driven 7th-semester B.Tech Computer Science student with practical experience building data-driven systems, "
        "machine learning models, and scalable backend REST APIs. Proficient in Python, SQL, Pandas, Scikit-learn, "
        "and FastAPI with strong knowledge of data structures, algorithms, and containerization with Docker.",
        body_style,
    ))
    story.append(Spacer(1, 4))

    # 3. Education
    story.append(Paragraph("EDUCATION", section_style))
    story.append(Paragraph("<b>B.Tech in Computer Science and Engineering</b> | Apex Institute of Technology (2021 - 2025)", body_style))
    story.append(Paragraph("CGPA: 8.8 / 10.0 | Relevant Coursework: Data Structures, Machine Learning, Database Management Systems, Operating Systems", body_style))
    story.append(Spacer(1, 4))

    # 4. Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_style))
    story.append(Paragraph("<b>Languages:</b> Python, C++, SQL, JavaScript", body_style))
    story.append(Paragraph("<b>Data Science & AI/ML:</b> Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Machine Learning, Deep Learning, Statistics", body_style))
    story.append(Paragraph("<b>Web & Backend:</b> FastAPI, Flask, REST API, HTML, CSS", body_style))
    story.append(Paragraph("<b>Databases & Tools:</b> PostgreSQL, MySQL, SQLite, Docker, Git, GitHub, Linux, Postman", body_style))
    story.append(Spacer(1, 4))

    # 5. Work Experience / Internships
    story.append(Paragraph("WORK EXPERIENCE", section_style))
    story.append(Paragraph("<b>Machine Learning Intern</b> | DataTech Analytics Labs (June 2024 - August 2024)", body_style))
    story.append(Paragraph("• Developed predictive customer retention models using Python and Scikit-learn, boosting prediction accuracy by 18%.", bullet_style))
    story.append(Paragraph("• Performed extensive exploratory data analysis and data cleaning on 120,000+ tabular records using Pandas and NumPy.", bullet_style))
    story.append(Paragraph("• Automated SQL data extraction queries from PostgreSQL database, reducing weekly report preparation time by 35%.", bullet_style))
    story.append(Paragraph("• Containerized analytical pipelines using Docker and tracked versions via Git and GitHub.", bullet_style))
    story.append(Spacer(1, 4))

    # 6. Projects
    story.append(Paragraph("TECHNICAL PROJECTS", section_style))
    story.append(Paragraph("<b>AI Resume Analyzer and Job Matching Platform</b> (Python, FastAPI, Scikit-learn, React)", body_style))
    story.append(Paragraph("• Implemented automated ATS compatibility scoring engine using TF-IDF vectorization and Cosine Similarity.", bullet_style))
    story.append(Paragraph("• Designed rule-based phrase matching algorithm to extract technical skills across 7 major software domains.", bullet_style))
    story.append(Paragraph("• Built asynchronous REST API microservices in FastAPI with JWT authentication and SQLAlchemy ORM.", bullet_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Automated Stock Market Forecasting Dashboard</b> (Python, Pandas, Streamlit, Scikit-learn)", body_style))
    story.append(Paragraph("• Built time-series forecasting regression models evaluating historical price trends with 85% directional accuracy.", bullet_style))
    story.append(Paragraph("• Designed interactive visual charts with Matplotlib and Seaborn for multi-asset portfolio comparisons.", bullet_style))
    story.append(Spacer(1, 4))

    # 7. Certifications & Achievements
    story.append(Paragraph("CERTIFICATIONS & ACHIEVEMENTS", section_style))
    story.append(Paragraph("• <b>Deep Learning Specialization</b> - Coursera / DeepLearning.AI", bullet_style))
    story.append(Paragraph("• <b>Python for Data Science and Machine Learning</b> - Udemy", bullet_style))
    story.append(Paragraph("• Ranked in Top 5% out of 4,000+ participants in National College Coding Hackathon 2024.", bullet_style))

    doc.build(story)
    print(f"Sample resume created successfully at: {OUTPUT_PDF}")


if __name__ == "__main__":
    create_sample_resume()
