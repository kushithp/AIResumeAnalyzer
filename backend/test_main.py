import pytest
from fastapi.testclient import TestClient
from app import app
from utils import extract_contact_info, categorize_skills
from parser import detect_sections, estimate_experience_level
from analyzer import compute_heuristic_analysis

client = TestClient(app)


def test_health_check():
    """Verify health check endpoint returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_frontend_is_served():
    """Verify the browser app and its static assets are available."""
    page = client.get("/app")
    assert page.status_code == 200
    assert "Resume Studio" in page.text
    assert client.get("/app/app.js").status_code == 200
    assert client.get("/app/styles.css").status_code == 200


def test_extract_contact_info():
    """Test contact extraction regex."""
    sample = "Jane Doe\nEmail: jane.doe@example.com\nPhone: (555) 123-4567\nExperienced developer"
    name, email, phone = extract_contact_info(sample)
    assert name == "Jane Doe"
    assert email == "jane.doe@example.com"
    assert "(555) 123-4567" in phone or "555" in phone


def test_detect_sections():
    """Test resume section detection."""
    sample_text = "Education\nB.S. Computer Science\nWork Experience\nSoftware Engineer at Tech Corp\nSkills\nPython, React"
    sections = detect_sections(sample_text)
    assert sections["Education"] is True
    assert sections["Experience"] is True
    assert sections["Skills"] is True


def test_heuristic_analysis():
    """Test deterministic ATS scoring computation."""
    resume_info = {
        "text": "John Developer\nPython, React, FastApi, Docker\nWork Experience at Google.",
        "candidate_name": "John Developer",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "extracted_skills": ["Python", "React", "FastAPI", "Docker"],
        "sections": {"Education": True, "Experience": True, "Skills": True, "Projects": True, "Certifications": False},
        "experience_level": "Junior"
    }
    jd = "Looking for a Python developer with React and FastAPI skills."
    res = compute_heuristic_analysis(resume_info, jd)

    assert res["score"] > 50
    assert "Python" in res["matching_skills"] or "React" in res["matching_skills"]
    assert len(res["checklist"]) > 0


def test_get_history_empty():
    """Test fetching history when DB is queried."""
    res = client.get("/api/history")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
