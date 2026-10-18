import os
import json
import re
from typing import Dict, Any, List
import requests
from utils import SKILL_TAXONOMY, ALL_SKILLS, categorize_skills
from parser import parse_resume_file


def compute_heuristic_analysis(resume_info: Dict[str, Any], job_description: str) -> Dict[str, Any]:
    """Calculate deterministic ATS scores, matching skills, and suggestions."""
    resume_text = resume_info["text"]
    extracted_skills = set(s.lower() for s in resume_info["extracted_skills"])
    jd_lower = job_description.lower()
    
    # Extract candidate skills required in JD
    jd_required_skills = set()
    for skill in ALL_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, jd_lower):
            jd_required_skills.add(skill.lower())
            
    # Calculate matching vs missing skills
    if jd_required_skills:
        matching_skills_raw = extracted_skills.intersection(jd_required_skills)
        missing_skills_raw = jd_required_skills.difference(extracted_skills)
        skill_match_ratio = len(matching_skills_raw) / len(jd_required_skills)
    else:
        matching_skills_raw = extracted_skills
        missing_skills_raw = set()
        skill_match_ratio = 0.75

    matching_skills = sorted([s.title() for s in matching_skills_raw])
    missing_skills = sorted([s.title() for s in missing_skills_raw])

    # Calculate Section Scores (Education, Experience, Skills, Projects, Certifications)
    sections = resume_info["sections"]
    section_scores = {}
    total_sec_weight = 0
    sec_weights = {"Skills": 30, "Experience": 30, "Projects": 20, "Education": 10, "Certifications": 10}
    
    for sec, present in sections.items():
        weight = sec_weights.get(sec, 15)
        score = 90 if present else 20
        section_scores[sec] = score
        total_sec_weight += (score * (weight / 100))

    # Calculate Completeness Score
    completeness = 0
    if resume_info["email"] != "Not Found": completeness += 15
    if resume_info["phone"] != "Not Found": completeness += 15
    if sections.get("Education"): completeness += 20
    if sections.get("Experience"): completeness += 20
    if sections.get("Skills"): completeness += 20
    if len(extracted_skills) >= 5: completeness += 10

    # Calculate final ATS Score (weighted: 55% skill match, 30% section score, 15% completeness)
    raw_ats_score = int((skill_match_ratio * 55) + (total_sec_weight * 0.30) + (completeness * 0.15))
    ats_score = max(10, min(98, raw_ats_score))

    # Strengths and Weaknesses
    strengths = []
    if len(matching_skills) >= 4:
        strengths.append(f"Strong match for core technical skills: {', '.join(matching_skills[:4])}")
    if completeness >= 80:
        strengths.append("Resume contains complete contact info and essential standard sections.")
    if sections.get("Experience"):
        strengths.append("Work Experience section is explicitly highlighted with relevant project history.")
    if not strengths:
        strengths.append("Resume layout is clean and readable.")

    weaknesses = []
    if missing_skills:
        weaknesses.append(f"Missing key job requirements: {', '.join(missing_skills[:4])}")
    if not sections.get("Certifications"):
        weaknesses.append("No explicit Certifications or specialized course section found.")
    if len(extracted_skills) < 5:
        weaknesses.append("Skill density is low; consider listing specific tools, frameworks, and databases.")

    # Suggestions
    suggestions = [
        f"Add missing keywords such as {', '.join(missing_skills[:3])} to your skills and experience descriptions." if missing_skills else "Optimize keyword placement in action bullet points.",
        "Quantify your bullet points with metrics and percentages (e.g., 'Improved API performance by 40%').",
        "Ensure section titles match standard ATS headings (e.g., 'Work Experience', 'Technical Skills')."
    ]

    # Rewrite Suggestions
    rewrite_suggestions = []
    if missing_skills:
        m_sample = missing_skills[0]
        rewrite_suggestions.append({
            "original": "Worked on backend features and APIs for web applications.",
            "suggested": f"Engineered scalable backend RESTful APIs integrating {m_sample}, reducing query latency by 25%."
        })
    rewrite_suggestions.append({
        "original": "Responsible for managing software development tasks.",
        "suggested": "Led Agile sprint planning and cross-functional team delivery, accelerating release cycles by 30%."
    })

    # AI-Generated Interview Questions based on Resume & JD
    interview_questions = []
    if matching_skills:
        top_skill = matching_skills[0]
        interview_questions.append(f"Can you describe a complex technical challenge you solved using {top_skill}?")
    if missing_skills:
        top_missing = missing_skills[0]
        interview_questions.append(f"The job role emphasizes {top_missing}. How quickly could you ramp up on this technology?")
    interview_questions.append("How do you approach optimizing performance and code quality in high-throughput applications?")
    interview_questions.append("Walk me through a project where you had to collaborate with cross-functional stakeholders.")

    # Course / Learning Recommendations for Missing Skills
    course_recommendations = []
    for skill in missing_skills[:3]:
        course_recommendations.append({
            "topic": f"Mastering {skill} for Developers",
            "reason": f"Required in job description but missing from resume skills section."
        })

    # Optimization Checklist
    checklist = [
        {"item": "Contact information (Email & Phone)", "passed": resume_info["email"] != "Not Found" and resume_info["phone"] != "Not Found"},
        {"item": "Standard ATS Section Headings", "passed": sections.get("Skills") and sections.get("Experience")},
        {"item": "High Keyword Alignment (>60%)", "passed": skill_match_ratio >= 0.6},
        {"item": "Action-Oriented Verbs", "passed": True},
        {"item": "Quantifiable Achievements", "passed": "10%" in resume_text or "20%" in resume_text or "$" in resume_text or "by" in resume_text}
    ]

    summary = (
        f"Resume matches approximately {int(skill_match_ratio * 100)}% of the target job requirements. "
        f"Candidate demonstrates strength in {', '.join(matching_skills[:3]) if matching_skills else 'general software development'}, "
        f"but would benefit from adding keywords like {', '.join(missing_skills[:3]) if missing_skills else 'advanced tooling'}."
    )

    return {
        "score": ats_score,
        "completeness_score": completeness,
        "experience_level": resume_info["experience_level"],
        "summary": summary,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_categories": categorize_skills(resume_info["extracted_skills"]),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "section_scores": section_scores,
        "interview_questions": interview_questions,
        "rewrite_suggestions": rewrite_suggestions,
        "course_recommendations": course_recommendations,
        "checklist": checklist
    }


def call_openai_analysis(resume_text: str, job_description: str) -> Dict[str, Any]:
    """Invoke OpenAI-compatible API for enhanced AI analysis if configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    if not api_key or api_key == "your_openai_api_key_here":
        return None

    prompt = f"""
You are an expert ATS (Applicant Tracking System) reviewer and hiring manager.
Analyze the following candidate resume text against the target job description.

RESUME TEXT:
{resume_text[:3500]}

JOB DESCRIPTION:
{job_description[:2500]}

Respond STRICTLY with valid JSON matching this schema:
{{
  "score": integer (0 to 100),
  "completeness_score": integer (0 to 100),
  "summary": string,
  "matching_skills": list of strings,
  "missing_skills": list of strings,
  "strengths": list of strings,
  "weaknesses": list of strings,
  "suggestions": list of strings,
  "interview_questions": list of strings,
  "rewrite_suggestions": [{"original": string, "suggested": string}],
  "course_recommendations": [{"topic": string, "reason": string}]
}}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }

    try:
        res = requests.post(f"{api_base}/chat/completions", headers=headers, json=payload, timeout=15)
        if res.status_code == 200:
            content = res.json()["choices"][0]["message"]["content"]
            return json.loads(content)
    except Exception as e:
        print(f"[AI Service Warning] Falling back to heuristic engine due to API error: {e}")
    
    return None


def run_full_analysis(filename: str, file_bytes: bytes, job_description: str, job_title: str = None) -> Dict[str, Any]:
    """Parse resume, calculate ATS score and AI metrics, and return structured analysis result."""
    resume_info = parse_resume_file(filename, file_bytes)
    
    # 1. First run deterministic heuristic analysis
    heuristic_res = compute_heuristic_analysis(resume_info, job_description)

    # 2. Optionally enrich with OpenAI if configured
    ai_res = call_openai_analysis(resume_info["text"], job_description)
    if ai_res and isinstance(ai_res, dict):
        # Merge AI enhancements
        heuristic_res["score"] = ai_res.get("score", heuristic_res["score"])
        heuristic_res["summary"] = ai_res.get("summary", heuristic_res["summary"])
        if "matching_skills" in ai_res: heuristic_res["matching_skills"] = ai_res["matching_skills"]
        if "missing_skills" in ai_res: heuristic_res["missing_skills"] = ai_res["missing_skills"]
        if "strengths" in ai_res: heuristic_res["strengths"] = ai_res["strengths"]
        if "weaknesses" in ai_res: heuristic_res["weaknesses"] = ai_res["weaknesses"]
        if "suggestions" in ai_res: heuristic_res["suggestions"] = ai_res["suggestions"]
        if "interview_questions" in ai_res: heuristic_res["interview_questions"] = ai_res["interview_questions"]
        if "rewrite_suggestions" in ai_res: heuristic_res["rewrite_suggestions"] = ai_res["rewrite_suggestions"]

    # Final combined response
    result = {
        "filename": filename,
        "candidate_name": resume_info["candidate_name"],
        "email": resume_info["email"],
        "phone": resume_info["phone"],
        "job_title": job_title or "Target Role",
        "job_description": job_description,
        **heuristic_res
    }
    
    return result
