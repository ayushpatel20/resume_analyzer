import io
from fastapi import status
from app.models.models import Resume


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"


def test_job_roles_endpoint(client):
    response = client.get("/api/job-roles")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "Data Analyst" in data
    assert "Data Scientist" in data


def test_sample_jds_endpoint(client):
    response = client.get("/api/sample-jds")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "Data Analyst" in data


def test_analyze_with_existing_resume(client, auth_headers, test_user, db_session):
    # Pre-create resume in database
    resume = Resume(
        user_id=test_user.id,
        filename="test_resume.pdf",
        file_path="uploads/test_resume.pdf",
        file_size=1024,
        extracted_text="""
        Jane Doe
        Email: jane.doe@example.com
        Phone: +1 555 123 4567
        
        SUMMARY
        Python Developer with expertise in FastAPI, PostgreSQL, Docker, and REST APIs.
        
        SKILLS
        Python, FastAPI, SQL, PostgreSQL, Docker, Git
        
        PROJECTS
        Built high-throughput microservices using FastAPI and Docker.
        
        EXPERIENCE
        Backend Developer at CloudCorp.
        """,
    )
    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    response = client.post(
        "/api/analysis/analyze",
        headers=auth_headers,
        data={
            "resume_id": resume.id,
            "job_title": "Backend Python Developer",
            "job_description": "We need a Python developer experienced with FastAPI, SQL, and Docker to develop microservices.",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["ats_score"] > 0
    assert data["resume_score"] > 0
    assert len(data["skills"]) > 0
    assert len(data["recommendations"]) > 0
    assert len(data["suggestions"]) > 0


def test_dashboard_stats(client, auth_headers):
    response = client.get("/api/analysis/dashboard-stats", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_resumes" in data
    assert "total_analyses" in data
