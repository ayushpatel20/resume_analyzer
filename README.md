# AI RESUME ANALYZER AND JOB MATCHING SYSTEM

> **A Full-Stack AI/NLP-Powered Web Application for Automated ATS Resume Evaluation, Skill Gap Discovery, and Career Role Recommendations**  
> *Final Year 7th-Semester B.Tech Mini Project in Computer Science & Engineering / Artificial Intelligence & Machine Learning*

---

## 1. Abstract
In modern hiring pipelines, Applicant Tracking Systems (ATS) automatically filter candidates before a human recruiter ever reviews their application. However, conventional commercial ATS tools function as opaque "black boxes" that reject qualified student candidates without constructive feedback. This project presents the **AI Resume Analyzer and Job Matching System**, a production-grade full-stack web application developed with **FastAPI**, **React.js**, **Tailwind CSS**, and **Scikit-learn**. The platform extracts text from PDF resumes using **PyMuPDF**, performs entity extraction and section recognition, matches technical proficiencies against customizable job descriptions, computes transparent ATS-style compatibility scores via **TF-IDF Vectorization** and **Cosine Similarity**, identifies missing skill gaps with ethical guidance, and generates downloadable **ReportLab** PDF evaluation reports.

---

## 2. Problem Statement
Job seekers and engineering graduates struggle to optimize their resumes for automated recruiting filters. Key pain points include:
1. **Opaque Scoring**: Candidates receive rejection notifications without knowing which keywords or skills were missing.
2. **Format Incompatibilities**: Complex multi-column templates cause text extraction failures in standard ATS parsers.
3. **Black-box Commercial Tools**: Existing commercial solutions rely on expensive, proprietary, or closed-source LLM APIs that cannot be explained or verified during academic evaluations.
4. **Unethical AI Hallucinations**: Generative LLM tools frequently advise candidates to add false credentials or fabricate quantifiable metrics.

---

## 3. Project Objectives
1. Build a robust, responsive web application connecting a **React + Vite** frontend with a **FastAPI** backend over REST APIs.
2. Implement local, private **PyMuPDF** text parsing capable of gracefully handling corrupt, empty, or scanned documents.
3. Engineer a transparent **ATS-Style Compatibility Scoring Algorithm** combining Semantic Text Similarity (50%), Skill Coverage (30%), and Keyword Match (20%).
4. Formulate an independent **0–100 Resume Quality Rubric** evaluating Contact, Summary, Education, Skills, Projects, Experience, Certifications, and Measurable Impact.
5. Provide a rule-based **Skill Gap Identifier** that ethically suggests missing technologies only if genuine experience exists.
6. Design an interactive **Job Role Recommendation Engine** evaluating compatibility against 8 curated software engineering profiles.
7. Deliver **ReportLab PDF Report Export** and a complete **JWT authentication** system with SQLite/PostgreSQL persistence.

---

## 4. Key Features
- **Modern SaaS Dashboard**: Sleek dark-mode interface built with Tailwind CSS, Lucide icons, and Recharts.
- **Instant Preloaded Job Descriptions**: One-click demo buttons for Data Analyst, Data Scientist, ML Engineer, Python Developer, and Software Developer roles.
- **Document Text Preview**: Direct in-browser modal viewer for inspected resume text extracted by PyMuPDF.
- **Multi-Stage Animated Pipeline**: Real-time visual progress indicator illustrating each evaluation phase.
- **Comprehensive History & Data Management**: Searchable historical evaluations, clear history controls, and profile deletion options.
- **Downloadable PDF Audit**: One-click generation of evaluation reports.

---

## 5. System Architecture

```
                               +----------------------------------------+
                               |        React Frontend (Vite)          |
                               |  Tailwind CSS | Recharts | Lucide     |
                               +-------------------+--------------------+
                                                   |
                                            JSON / REST APIs
                                                   |
                                                   v
+--------------------------------------------------------------------------------------------------+
|                                    FastAPI Backend Service                                       |
|                                                                                                  |
|   +-------------------+   +--------------------+   +--------------------+   +----------------+   |
|   |   JWT Security    |   |   PDF Extraction   |   |   Database ORM     |   |   ReportLab    |   |
|   |  Bcrypt / Tokens  |   | PyMuPDF / Cleaners |   |   SQLAlchemy 2.0   |   |  PDF Generator |   |
|   +-------------------+   +--------------------+   +--------------------+   +----------------+   |
|                                                                                                  |
|   +------------------------------------------------------------------------------------------+   |
|   |                                  Core NLP & AI Engine                                    |   |
|   |  TF-IDF Vectorizer | Cosine Similarity | Boundary Skill Matcher | 0-100 Quality Scorer   |   |
|   |  Entity Extractor  | Section Parser    | Role Recommender       | Ethical Suggestions    |   |
|   +------------------------------------------------------------------------------------------+   |
+--------------------------------------------------+-----------------------------------------------+
                                                   |
                                                   v
                               +----------------------------------------+
                               |          Database Layer                |
                               |  SQLite (Default) / PostgreSQL (Env)  |
                               +----------------------------------------+
```

---

## 6. Technology Stack

| Layer | Technologies Used | Justification |
| :--- | :--- | :--- |
| **Frontend** | React 19, Vite, Tailwind CSS, Lucide React, Recharts, Axios | Ultra-fast build times, responsive SaaS design, rich interactive data charts. |
| **Backend** | Python 3.12, FastAPI, Uvicorn, Pydantic V2 | High-performance asynchronous REST endpoints, automatic Swagger UI documentation. |
| **Database** | SQLite (Default), PostgreSQL (Supported), SQLAlchemy 2.0 | Zero-configuration instant local development with production enterprise compatibility. |
| **PDF Processing** | PyMuPDF (`fitz`), `pypdf` | Rapid C-level PDF parsing and layout cleaning. |
| **AI / NLP** | Scikit-learn, TF-IDF Vectorizer, Cosine Similarity, Regex | Explainable, reproducible, viva-friendly algorithms without third-party API costs. |
| **PDF Reporting**| ReportLab | Direct server-side compilation of styled PDF evaluation dossiers. |
| **Security** | Direct Bcrypt Hashing, PyJWT (HMAC-SHA256) | Robust credential protection and stateless session authorization. |

---

## 7. AI & NLP Methodology
1. **Text Normalization**: Strips non-printable ASCII, normalizes unicode whitespace, collapses excess line breaks, and preserves semantic indentation.
2. **Rule-Based Skill Extraction**: Regular expressions with strict word boundaries (`(?<!\w)skill(?!\w)`) match against a curated library of 100+ technologies across 7 domains. Special handling prevents false matches (e.g. `C++`, `C#`, `.NET`, and single-letter `C` or `R`).
3. **Entity Extraction**: Heuristic patterns extract candidate name, email, phone numbers (including Indian +91 and international formats), degree certifications, GitHub, and LinkedIn links.
4. **Section Parsing**: Heading pattern recognition evaluates the presence of Summary, Objective, Education, Skills, Experience, Projects, Certifications, and Achievements.

---

## 8. ATS-Style Compatibility Scoring Formula

The system implements a transparent, weighted formula designed for academic evaluation:

$$\text{ATS Score} = (0.50 \times S_{\text{semantic}}) + (0.30 \times S_{\text{skills}}) + (0.20 \times S_{\text{keywords}})$$

Where:
- **$S_{\text{semantic}}$ (TF-IDF Cosine Similarity)**: Measures textual alignment between the resume and job description using word and bi-gram frequencies:
  $$\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2} \times 100$$
- **$S_{\text{skills}}$ (Skill Match Ratio)**:
  $$S_{\text{skills}} = \left( \frac{\text{Matched Required Skills}}{\text{Total Required Skills in Job Description}} \right) \times 100$$
- **$S_{\text{keywords}}$ (Domain Keyword Coverage)**: Percentage of top non-stopword domain keywords appearing in the resume.

---

## 9. Resume Quality Score Rubric (0–100)

| Evaluation Dimension | Maximum Points | Verification Criteria |
| :--- | :---: | :--- |
| **Contact Information** | 10 pts | Email (3), Phone (3), LinkedIn (2), GitHub (2) |
| **Summary / Objective** | 10 pts | Concise professional summary or career objective present |
| **Education** | 10 pts | Academic institution, graduation year, and degree qualification |
| **Technical Skills** | 15 pts | Dedicated technical skills section with 10+ identified proficiencies |
| **Projects** | 15 pts | Documented technical projects with implementation details and tools |
| **Work Experience** | 15 pts | Employment, internship, or technical role history |
| **Certifications** | 10 pts | Industry certifications or accredited technical coursework |
| **Achievements** | 5 pts | Academic honors, hackathon awards, or publications |
| **Quantifiable Impact** | 10 pts | Action verbs and measurable impact indicators (e.g., `%`, `$`, `+`) |
| **Total Quality Score** | **100 pts** | Comprehensive structural rubric |

---

## 10. Database Schema Design

```
+------------------+         +--------------------+         +-------------------+
|      USERS       | 1     * |      RESUMES       | 1     * |     ANALYSES      |
|------------------|---------|--------------------|---------|-------------------|
| id (PK)          |         | id (PK)            |         | id (PK)           |
| name             |         | user_id (FK)       |         | user_id (FK)      |
| email (Unique)   |         | filename           |         | resume_id (FK)    |
| password_hash    |         | file_path          |         | job_title         |
| created_at       |         | file_size          |         | job_description   |
| updated_at       |         | extracted_text     |         | ats_score         |
+------------------+         | uploaded_at        |         | resume_score      |
                             +--------------------+         | skill_match_score |
                                                            | keyword_score     |
                                                            | semantic_score    |
                                                            | extracted_info    |
                                                            | detected_sections |
                                                            | score_breakdown   |
                                                            | created_at        |
                                                            +---------+---------+
                                                                      | 1
                                                                      |
                                       +------------------------------+------------------------------+
                                       | 1                          * | 1                          * | 1                          *
                             +---------v----------+         +---------v----------+         +---------v----------+
                             |  ANALYSIS_SKILLS   |         |  RECOMMENDATIONS   |         |    SUGGESTIONS     |
                             |--------------------|         |--------------------|         |--------------------|
                             | id (PK)            |         | id (PK)            |         | id (PK)            |
                             | analysis_id (FK)   |         | analysis_id (FK)   |         | analysis_id (FK)   |
                             | skill_name         |         | job_role           |         | category           |
                             | category           |         | score              |         | suggestion         |
                             | status             |         | matched_skills     |         +--------------------+
                             +--------------------+         | missing_skills     |
                                                            +--------------------+
```

---

## 11. Folder Structure

```
resume_analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application & route registration
│   │   ├── config.py               # Settings & configurable weights
│   │   ├── database.py             # SQLAlchemy engine & session maker
│   │   ├── models/models.py        # Database entities & relationships
│   │   ├── schemas/                # Pydantic V2 validation schemas
│   │   ├── auth/                   # Bcrypt password hashing & JWT handlers
│   │   ├── services/
│   │   │   ├── pdf_service.py      # PyMuPDF text extractor
│   │   │   └── report_service.py   # ReportLab PDF dossier generator
│   │   ├── ml/
│   │   │   ├── skill_extractor.py  # Regex word-boundary skill detector
│   │   │   ├── section_parser.py   # Heading parser for resume sections
│   │   │   ├── info_extractor.py   # Contact & degree entity extractor
│   │   │   ├── matcher.py          # TF-IDF & ATS scoring engine
│   │   │   ├── scorer.py           # 0-100 Resume Quality rubric
│   │   │   ├── recommender.py      # Career role recommendation engine
│   │   │   └── suggestion_engine.py# Ethical resume improvement tips
│   │   └── routers/                # REST API controllers
│   ├── tests/                      # Pytest automated test suite (19 tests)
│   ├── requirements.txt            # Backend Python dependencies
│   ├── run.py                      # Uvicorn quick runner script
│   └── Dockerfile                  # Container definition
│
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # Landing, Auth, Dashboard, Analysis, Results, History
│   │   ├── context/AuthContext.jsx # Global JWT authentication state
│   │   ├── services/api.js         # Axios client with bearer interceptors
│   │   ├── App.jsx                 # Route configuration
│   │   └── index.css               # Tailwind CSS directives
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── data/
│   ├── skills.json                 # 100+ categorized skills library
│   ├── job_roles.json              # Curated career role definitions
│   ├── sample_job_descriptions.json# Preloaded realistic job descriptions
│   └── sample_resume.pdf           # Pre-generated PDF resume for instant demo
│
├── uploads/                        # Secure local storage for uploaded resumes
├── reports/                        # Compiled ReportLab PDF reports
├── docker-compose.yml              # Optional containerized deployment
├── .env.example                    # Environment template
└── README.md                       # Project documentation
```

---

## 12. Installation & Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Node.js v18+ and npm

### 1. Clone or Navigate to Directory
```bash
cd resume_analyzer
```

### 2. Backend Setup
```powershell
# Create Python virtual environment
python -m venv backend/venv

# Activate virtual environment
# On Windows:
backend\venv\Scripts\activate
# On Linux/macOS:
source backend/venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 3. Frontend Setup
```powershell
cd frontend
npm install
cd ..
```

---

## 13. Running the Application

### Start Backend Service
```powershell
# From project root:
backend\venv\Scripts\python.exe backend/run.py
```
*Backend runs at:* `http://127.0.0.1:8000`  
*Interactive Swagger Documentation:* `http://127.0.0.1:8000/docs`

### Start Frontend Service
```powershell
# Open a second terminal window:
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
*Frontend runs at:* `http://127.0.0.1:5173`

---

## 14. Sample Usage & Quick Demo
1. Open `http://127.0.0.1:5173` in your browser.
2. Click **Get Started** and create an account (e.g. `student@example.com` / `password123`).
3. On the **Dashboard**, click **Start New Analysis**.
4. In **Step 1**, upload the sample resume provided in `data/sample_resume.pdf`.
5. In **Step 2**, click any of the sample role buttons (e.g., **Machine Learning Engineer** or **Data Scientist**) to instantly populate a realistic industry job description.
6. Click **Analyze Resume Now**.
7. Observe the multi-stage evaluation animation, then view your comprehensive scores, matched skills, missing skill gaps, section checklist, charts, and recommendations.
8. Click **Download PDF Report** to verify server-side PDF generation.

---

## 15. Automated Testing Suite

The project includes 19 comprehensive pytest tests verifying authentication, PDF extraction, NLP modules, and REST endpoints.

To run the test suite:
```powershell
backend\venv\Scripts\pytest.exe backend/tests/ -v
```

Expected output:
```
backend/tests/test_api.py::test_health_check PASSED                      [  5%]
backend/tests/test_api.py::test_job_roles_endpoint PASSED                [ 10%]
backend/tests/test_api.py::test_sample_jds_endpoint PASSED               [ 15%]
backend/tests/test_api.py::test_analyze_with_existing_resume PASSED      [ 21%]
backend/tests/test_api.py::test_dashboard_stats PASSED                   [ 26%]
backend/tests/test_auth.py::test_register_user PASSED                    [ 31%]
backend/tests/test_auth.py::test_register_duplicate_email PASSED         [ 36%]
backend/tests/test_auth.py::test_login_success PASSED                    [ 42%]
backend/tests/test_auth.py::test_login_wrong_password PASSED             [ 47%]
backend/tests/test_auth.py::test_get_current_user PASSED                 [ 52%]
backend/tests/test_auth.py::test_unauthorized_access PASSED              [ 57%]
backend/tests/test_nlp.py::test_skill_extraction PASSED                  [ 63%]
backend/tests/test_nlp.py::test_special_skill_c_plus_plus PASSED         [ 68%]
backend/tests/test_nlp.py::test_section_parsing PASSED                   [ 73%]
backend/tests/test_nlp.py::test_info_extraction PASSED                   [ 78%]
backend/tests/test_nlp.py::test_ats_matching PASSED                      [ 84%]
backend/tests/test_nlp.py::test_job_recommendation PASSED                [ 89%]
backend/tests/test_pdf.py::test_invalid_extension PASSED                 [ 94%]
backend/tests/test_pdf.py::test_empty_file PASSED                        [100%]
======================= 19 passed in 3.23s =======================
```

---

## 16. Security & Privacy Considerations
- **No External Cloud API Leaks**: Resume texts are parsed locally and never transmitted to external third-party AI APIs.
- **Password Security**: Passwords are encrypted using salted bcrypt hashing and truncated at 72 bytes. Plaintext passwords are never saved or logged.
- **Access Control**: Users can only access resumes, reports, and analyses associated with their authenticated account ID.
- **Sanitization**: Uploaded filenames are sanitized and stored with randomized UUID prefixes to prevent path traversal attacks.

---

## 17. Ethical Recommendations & Anti-Hallucination Policy
Unlike generative AI assistants that may fabricate achievements, this platform:
- Displays missing skills with the explicit instruction: *"Consider adding this skill only if you genuinely have project or professional experience with it."*
- Strictly extracts existing credentials without inventing degrees, dates, or companies.
- Transparently breaks down mathematical scoring weights to aid candidates during academic viva voce evaluations.

---

## 18. Known Limitations
1. **Scanned / Image PDFs**: Resumes that are flat scanned images without an embedded text layer require OCR (e.g. Tesseract) to parse. The system detects scanned PDFs and prompts the user for a text-based file.
2. **Heuristic Name Extraction**: Highly decorative, graphic resumes with unconventional layouts may require manual profile adjustment.
3. **English Language Focus**: Current skill and keyword tokenizers are optimized for English technical documents.

---

## 19. Future Scope
- Integration of Optical Character Recognition (OCR) using Tesseract for scanned legacy resumes.
- Transformer-based embeddings (e.g., Sentence-BERT) for deeper contextual semantic similarity.
- Integration of live web job board APIs (LinkedIn, Indeed, Adzuna) for automated real-time vacancy matching.
- Interactive interview question generator based on detected resume skill gaps.

---

## 20. Viva Voce Q&A Cheat-Sheet

**Q1: How is the ATS score calculated?**  
*Answer*: The system combines 50% TF-IDF Cosine Similarity (measuring overall textual and semantic vocabulary alignment), 30% Skill Coverage (ratio of matched required technical skills from the job description), and 20% Keyword Coverage (presence of key domain terms).

**Q2: Why not use OpenAI or Gemini API for scoring?**  
*Answer*: LLM APIs are proprietary, costly, variable across invocations, and act as black boxes. By using TF-IDF and rule-based token boundary extraction, the mathematical decisions are 100% deterministic, explainable, and runnable locally with zero operating expense.

**Q3: How do you prevent false skill matches like "SQL" matching "GraphQL" or "C" matching "etc"?**  
*Answer*: The `SkillExtractor` module utilizes regex negative lookbehinds and lookaheads (`(?<!\w)skill(?!\w)`), sorts multi-word phrases by descending length, and implements specialized symbol regexes for `C++`, `C#`, and single-letter languages.

---

*AI Resume Analyzer and Job Matching System &bull; 7th Semester B.Tech Mini Project &bull; 2026*
