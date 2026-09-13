# B.TECH MINI PROJECT DOCUMENTATION
## AI RESUME ANALYZER AND JOB MATCHING SYSTEM

**Degree**: Bachelor of Technology (B.Tech) in Computer Science and Engineering / Artificial Intelligence  
**Academic Semester**: 7th Semester  
**Subject**: Mini Project / Minor Project  
**Academic Year**: 2025–2026  

---

### TABLE OF CONTENTS
1. [Chapter 1: Introduction](#chapter-1-introduction)
2. [Chapter 2: Problem Statement](#chapter-2-problem-statement)
3. [Chapter 3: Objectives](#chapter-3-objectives)
4. [Chapter 4: Existing System Analysis](#chapter-4-existing-system-analysis)
5. [Chapter 5: Proposed System Architecture](#chapter-5-proposed-system-architecture)
6. [Chapter 6: Literature & Technology Overview](#chapter-6-literature--technology-overview)
7. [Chapter 7: System Requirements Specification](#chapter-7-system-requirements-specification)
8. [Chapter 8: System Architecture & Data Flow](#chapter-8-system-architecture--data-flow)
9. [Chapter 9: Methodology & Mathematical Modeling](#chapter-9-methodology--mathematical-modeling)
10. [Chapter 10: Implementation Details](#chapter-10-implementation-details)
11. [Chapter 11: Experimental Results & Analysis](#chapter-11-experimental-results--analysis)
12. [Chapter 12: Software Testing & Verification](#chapter-12-software-testing--verification)
13. [Chapter 13: Limitations](#chapter-13-limitations)
14. [Chapter 14: Future Scope](#chapter-14-future-scope)
15. [Chapter 15: Conclusion & References](#chapter-15-conclusion--references)

---

## Chapter 1: Introduction
In the contemporary talent acquisition landscape, automated software systems process over 75% of job applications submitted to medium and large organizations. These systems, collectively known as **Applicant Tracking Systems (ATS)**, ingest resumes, parse textual sections, search for required technical competencies, and rank applicants prior to human intervention.

Despite the widespread utilization of ATS software by employers, prospective job seekers—specifically undergraduate engineering students and early-career software engineers—lack access to reliable, transparent diagnostic tools. Commercial ATS tools are frequently proprietary, cost-prohibitive, and withhold the quantitative criteria dictating candidate ranking.

This academic project presents the **AI Resume Analyzer and Job Matching System**, a full-stack web application that democratizes resume evaluation. Utilizing Natural Language Processing (NLP), rule-based skill boundary extraction, Term Frequency-Inverse Document Frequency (TF-IDF) vectorization, and Cosine Similarity metrics, the system delivers verifiable, explainable compatibility scores alongside constructive, ethical recommendations.

---

## Chapter 2: Problem Statement
Modern automated recruitment workflows present multiple systemic challenges for candidates:
1. **The "Black Box" Dilemma**: Candidates receiving automated rejection emails receive zero feedback regarding the specific technical gaps or formatting errors that disqualified their submission.
2. **Format and Encoding Vulnerabilities**: Multi-column layouts, tabular resume designs, and embedded graphical icons frequently fail in standard text extraction pipelines, resulting in zero detected skills.
3. **Dependence on Costly External APIs**: Existing academic mockups often rely on commercial third-party LLM APIs (e.g. OpenAI GPT-4). This introduces significant privacy concerns regarding the leakage of Personally Identifiable Information (PII), introduces unpredictable recurring costs, and prevents local offline execution.
4. **Hallucination of Qualifications**: Generative AI tools often advise candidates to fabricate achievements or claim experience with technologies they have never utilized.

---

## Chapter 3: Objectives
The primary objectives of this project are:
1. **Full-Stack Integration**: Construct a modern, decoupled web application utilizing **FastAPI** for backend REST API orchestration and **React.js (Vite)** with **Tailwind CSS** for the responsive user dashboard.
2. **Text Extraction Pipeline**: Implement local PDF parsing with **PyMuPDF**, incorporating cleaning heuristics for whitespace normalization and graceful error handling for unreadable or scanned files.
3. **Transparent ATS Scoring**: Develop an explainable mathematical formula combining:
   - 50% TF-IDF Cosine Semantic Similarity
   - 30% Skill Coverage Ratio
   - 20% Domain Keyword Coverage
4. **Objective 0–100 Quality Rubric**: Establish a standard evaluation metric assessing Contact Details, Summary, Education, Skills, Projects, Work Experience, Certifications, and Measurable Metric Quantifiers.
5. **Skill Gap Identification**: Detect missing technical skills specified in the target Job Description and present actionable, ethical improvement guidance.
6. **Career Role Recommendations**: Map candidate skills against curated software engineering profiles (Data Scientist, ML Engineer, Python Developer, etc.) and calculate percentage compatibility.
7. **Report Compilation**: Generate downloadable **ReportLab** PDF evaluation reports summarizing candidate diagnostics for offline review.

---

## Chapter 4: Existing System Analysis

### 4.1 Characteristics of Current Systems
- **Commercial ATS Systems (Workday, Taleo, Greenhouse)**: Designed exclusively for recruiters to filter out large volumes of candidates; inaccessible to job seekers for pre-submission diagnostics.
- **Online Commercial Resume Scanners (Jobscan, ResumeWorded)**: Offer limited free tier checks, gate critical keyword diagnostics behind monthly subscriptions, and operate on proprietary algorithms.
- **Open-Source Streamlit Scripts**: Provide simple one-off Python scripts lacking real database persistence, user authentication, interactive dashboards, or full-stack architectural separation.

### 4.2 Comparative Analysis

| Dimension | Commercial ATS | Commercial Scanners | Streamlit Scripts | **Proposed System** |
| :--- | :--- | :--- | :--- | :--- |
| **User Orientation** | Employer-only | Candidate | Developer-only | **Candidate & Student** |
| **Cost** | High Enterprise | Subscription ($30+/mo)| Free | **100% Free & Open Source** |
| **Explainability** | Hidden | Proprietary | Variable | **Fully Mathematical & Documented** |
| **Data Privacy** | Cloud Hosted | Third-Party Stored | Local | **Local Storage / Zero API Leakage** |
| **Authentication** | Enterprise SSO | Basic | None | **JWT + Bcrypt Security** |
| **Architecture** | Monolithic Cloud | Cloud Web App | Single Script | **Decoupled FastAPI + React REST** |

---

## Chapter 5: Proposed System Architecture
The proposed system addresses the shortcomings of existing tools through a clean, decoupled client-server architecture:

1. **Client Tier (React Vite SPA)**:
   - Interactive SaaS landing page, registration/login portals, and candidate dashboard.
   - Drag-and-drop resume upload zone with instant preloaded sample job descriptions.
   - Visual analytics utilizing Recharts (Quality Score breakdown and Role compatibility).
2. **Application Tier (FastAPI REST Service)**:
   - Asynchronous request handling and dependency-injected session management.
   - PyMuPDF text extraction with regex layout cleaners.
   - Scikit-learn TF-IDF Vectorizer and Cosine Similarity calculation.
   - ReportLab PDF compilation service.
3. **Data Tier (Relational Storage)**:
   - Default SQLite database for instant, zero-friction local demonstration.
   - Production PostgreSQL compatibility via environment variable configuration.

---

## Chapter 6: Literature & Technology Overview

### 6.1 Natural Language Processing (NLP) & Information Retrieval
- **Term Frequency-Inverse Document Frequency (TF-IDF)**: An established numerical statistic reflecting how important a word is to a document within a corpus.
- **Cosine Similarity**: A metric measuring the cosine of the angle between two non-zero vectors projected in a multi-dimensional space, providing length-invariant semantic similarity.

### 6.2 Framework Selection
- **FastAPI**: Chosen over Flask and Django due to native asynchronous execution, automatic OpenAPI Swagger documentation generation (`/docs`), and robust Pydantic data validation.
- **PyMuPDF (`fitz`)**: Outperforms traditional Python PDF tools (such as PyPDF2) by executing high-performance C-level parsing of complex font encodings and multi-page layouts.
- **React.js & Vite**: Provides modular component hierarchy, rapid Hot Module Replacement (HMR), and lightweight client-side state management via React Context.

---

## Chapter 7: System Requirements Specification

### 7.1 Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher (2.0 GHz+).
- **RAM**: Minimum 4 GB (8 GB recommended for concurrent Vite & Uvicorn dev servers).
- **Storage**: Minimum 500 MB free disk space.

### 7.2 Software Requirements
- **Operating System**: Windows 10/11, macOS, or Linux (Ubuntu 20.04+).
- **Runtime Environment**: Python 3.10 to 3.12, Node.js v18.0.0+.
- **Browser**: Modern Chromium-based browser (Chrome, Edge) or Firefox.
- **Database**: SQLite 3 (included with Python) or PostgreSQL 14+.

---

## Chapter 8: System Architecture & Data Flow

### 8.1 Data Flow Diagram (DFD Level 1)

```
[Candidate] ---> (1.0 Upload PDF & Target JD) ---> [PyMuPDF Parser]
                                                          |
                                                    Extracted Text
                                                          |
                                                          v
                                               (2.0 Information Extractor)
                                               - Name, Email, Phone, Links
                                               - Detected Sections Checklist
                                                          |
                                                          v
                                               (3.0 NLP & Matching Engine)
                                               - TF-IDF Vectorizer
                                               - SkillExtractor (100+ Skills)
                                               - ATS Matcher (50-30-20 Formula)
                                               - 0-100 Quality Scorer
                                                          |
                                                          v
                                               (4.0 Database Persistence)
                                               - SQLite / PostgreSQL
                                                          |
                                                          v
[Candidate] <--- (5.0 Interactive Dashboard & PDF Report) <---
```

---

## Chapter 9: Methodology & Mathematical Modeling

### 9.1 Text Preprocessing Pipeline
Raw extracted PDF text undergoes sequential normalization:
1. `\r\n` and `\r` carriage returns replaced with `\n`.
2. Non-printable control characters removed while retaining whitespace structure.
3. Excessive contiguous blank lines consolidated to a maximum of two.
4. Intra-line spacing normalized to single whitespace.

### 9.2 TF-IDF Cosine Similarity Computation
Let document vector $\mathbf{R}$ represent the candidate's normalized resume and vector $\mathbf{J}$ represent the target job description. The TF-IDF weight for term $t$ in document $d$ is:

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left( \frac{1 + |D|}{1 + \text{DF}(t, D)} \right) + 1$$

The semantic similarity percentage $S_{\text{semantic}} \in [0, 100]$ is computed as:

$$S_{\text{semantic}} = \left( \frac{\sum_{i=1}^{n} R_i J_i}{\sqrt{\sum_{i=1}^{n} R_i^2} \sqrt{\sum_{i=1}^{n} J_i^2}} \right) \times 100$$

### 9.3 Skill Match Percentage
Given the set of required technical skills detected in the job description $\mathcal{S}_{\text{JD}}$ and the set of skills detected in the resume $\mathcal{S}_{\text{Resume}}$:

$$\mathcal{S}_{\text{matched}} = \mathcal{S}_{\text{Resume}} \cap \mathcal{S}_{\text{JD}}$$

$$S_{\text{skills}} = \begin{cases} 
\left( \frac{|\mathcal{S}_{\text{matched}}|}{|\mathcal{S}_{\text{JD}}|} \right) \times 100 & \text{if } |\mathcal{S}_{\text{JD}}| > 0 \\
\min(100.0, |\mathcal{S}_{\text{Resume}}| \times 8.0) & \text{otherwise}
\end{cases}$$

### 9.4 Final ATS Compatibility Score
$$S_{\text{ATS}} = (0.50 \times S_{\text{semantic}}) + (0.30 \times S_{\text{skills}}) + (0.20 \times S_{\text{keywords}})$$

---

## Chapter 10: Implementation Details

### 10.1 Backend Implementation Highlights
- **FastAPI Dependency Injection**: `get_current_user` decodes incoming Bearer JWT tokens, verifies expiration, and injects the database user model.
- **Safe Regex Matching**: `SkillExtractor` sorts skills by descending character length to ensure multi-word phrases (e.g. "Machine Learning") match before sub-tokens (e.g. "Learning"). Single-character and punctuation languages (`C++`, `C#`, `C`, `R`) utilize boundary assertion patterns.
- **ReportLab PDF Generator**: `ReportService` defines custom `ParagraphStyle` structures, tables, and palette colors to compile consistent evaluation summaries.

### 10.2 Frontend Implementation Highlights
- **Auth Context**: `AuthContext.jsx` manages persistent login states via `localStorage`, executing silent token renewal and handling 401 redirects.
- **Multi-Stage Loader**: `LoadingAnalysis.jsx` renders an animated progress modal that cycles through 7 distinct pipeline stages during API execution.
- **Responsive Layout**: Designed with Tailwind CSS utility classes, supporting mobile drawer navigation and desktop split views.

---

## Chapter 11: Experimental Results & Analysis

### 11.1 Test Case Scenario: 4th Year B.Tech Computer Science Resume
- **Candidate Evaluated**: Atharv Shukla (B.Tech CSE)
- **Target Role Evaluated**: Machine Learning Engineer
- **Observed Metrics**:
  - **ATS Compatibility Score**: 32.0%
  - **Resume Quality Score**: 88.0 / 100
  - **Skill Match Score**: 44.0% (7 Matched out of 16 target skills)
  - **Keyword Match Score**: 60.0%
  - **Matched Skills**: Python, FastAPI, Machine Learning, PyTorch, TensorFlow, Scikit-learn, Scikit-Learn
  - **Identified Missing Gaps**: Docker, Git, Kubernetes, Linux, Deep Learning, Computer Vision, NLP, Microservices
  - **Role Recommendations**:
    1. Data Scientist (55% Fit)
    2. Machine Learning Engineer (52% Fit)
    3. AI Engineer (45% Fit)
    4. Software Developer (32% Fit)

### 11.2 Visual Diagnostics Rendered
The platform generated circular progress gauges, Recharts horizontal bar charts for role compatibility, and an itemized breakdown of the 0–100 quality rubric.

---

## Chapter 12: Software Testing & Verification

### 12.1 Testing Methodology
Automated unit and integration tests were developed using **pytest** and the FastAPI `TestClient`, utilizing an in-memory SQLite database (`sqlite:///:memory:`) for test isolation.

### 12.2 Test Matrix Summary

| Test Module | Test Name | Target Tested | Result |
| :--- | :--- | :--- | :---: |
| `test_auth.py` | `test_register_user` | User creation & JWT generation | **PASSED** |
| `test_auth.py` | `test_register_duplicate_email` | Duplicate email rejection (400) | **PASSED** |
| `test_auth.py` | `test_login_success` | Bcrypt password verification | **PASSED** |
| `test_auth.py` | `test_login_wrong_password` | Invalid credentials handling (401) | **PASSED** |
| `test_auth.py` | `test_get_current_user` | Bearer token authorization header | **PASSED** |
| `test_auth.py` | `test_unauthorized_access` | Unauthenticated route rejection | **PASSED** |
| `test_nlp.py` | `test_skill_extraction` | Normalized skill keyword detection | **PASSED** |
| `test_nlp.py` | `test_special_skill_c_plus_plus`| Boundary regex for `C++` and `C#` | **PASSED** |
| `test_nlp.py` | `test_section_parsing` | Heading pattern recognition | **PASSED** |
| `test_nlp.py` | `test_info_extraction` | Phone, Email, Degree parsing | **PASSED** |
| `test_nlp.py` | `test_ats_matching` | TF-IDF Cosine Similarity calculation | **PASSED** |
| `test_nlp.py` | `test_job_recommendation` | Role compatibility ranking | **PASSED** |
| `test_pdf.py` | `test_invalid_extension` | Rejection of non-PDF uploads | **PASSED** |
| `test_pdf.py` | `test_empty_file` | Rejection of 0-byte files | **PASSED** |
| `test_api.py` | `test_health_check` | Service readiness endpoint | **PASSED** |
| `test_api.py` | `test_job_roles_endpoint` | Curated job roles delivery | **PASSED** |
| `test_api.py` | `test_sample_jds_endpoint` | Preloaded sample job descriptions | **PASSED** |
| `test_api.py` | `test_analyze_with_existing_resume` | Full end-to-end analysis execution | **PASSED** |
| `test_api.py` | `test_dashboard_stats` | Aggregated user dashboard KPIs | **PASSED** |

**Total Tests**: 19 Passed, 0 Failed (100% Success Rate in 3.23s).

---

## Chapter 13: Limitations
1. **Optical Character Recognition (OCR)**: Scanned image resumes without embedded text layers require external OCR engines to extract raw characters.
2. **Graphic and Icon Formats**: Decorative infographics or timeline charts cannot be decoded without computer vision models.
3. **Language Scope**: Current skill dictionaries and stopword sets are configured specifically for English-language documents.

---

## Chapter 14: Future Scope
1. **Tesseract OCR Integration**: Integrate open-source OCR preprocessing to support image-based and scanned resumes.
2. **Contextual Sentence Transformers**: Integrate fine-tuned embeddings (e.g. S-BERT) to measure conceptual alignment beyond token-frequency overlap.
3. **Live Job Market Web Crawlers**: Connect to public job APIs to retrieve real-time job openings matching the candidate's top recommended roles.
4. **Personalized Upskilling Roadmaps**: Automatically generate curated GitHub repository links and free course recommendations for identified skill gaps.

---

## Chapter 15: Conclusion & References

### 15.1 Conclusion
The **AI Resume Analyzer and Job Matching System** fulfills all requirements for a 7th-semester B.Tech mini project. By uniting modern full-stack development practices (FastAPI, React, Tailwind CSS) with classical, explainable NLP algorithms (TF-IDF, Cosine Similarity, rule-based extraction), the system delivers transparent ATS diagnostics and career guidance. The platform operates 100% locally with zero external API dependencies, ensuring candidate privacy and reproducible demonstration during academic viva examinations.

### 15.2 References
1. Salton, G., & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval*. Information Processing & Management, 24(5), 513-523.
2. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
3. Ramirez, T. (2020). *FastAPI: Modern, High-Performance Web Framework for Python*. Tiangolo.
4. ReportLab Inc. (2024). *ReportLab PDF Generation User Guide*. ReportLab Open Source Documentation.

---
*Documentation compiled for academic mini-project submission &bull; Department of Computer Science & Engineering*
