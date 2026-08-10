import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from database import get_db
from models import Analysis
from schemas import AnalysisResponse, AnalysisListItem, DashboardStats
from parser import parse_resume_file
from analyzer import run_full_analysis, categorize_skills

router = APIRouter(prefix="/api", tags=["Resume Analyzer"])


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload PDF or DOCX resume and return extracted text and preview metadata."""
    if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a PDF or DOCX file."
        )

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 10MB."
        )

    try:
        parsed_info = parse_resume_file(file.filename, file_bytes)
        return {
            "filename": file.filename,
            "candidate_name": parsed_info["candidate_name"],
            "email": parsed_info["email"],
            "phone": parsed_info["phone"],
            "extracted_skills": parsed_info["extracted_skills"],
            "sections": parsed_info["sections"],
            "experience_level": parsed_info["experience_level"],
            "text_preview": parsed_info["text"][:600] + "..." if len(parsed_info["text"]) > 600 else parsed_info["text"]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: Optional[str] = Form("Target Role"),
    db: Session = Depends(get_db)
):
    """Run full ATS analysis on uploaded resume against a job description, saving the result."""
    if not job_description or len(job_description.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid Job Description (minimum 10 characters)."
        )

    file_bytes = await file.read()
    try:
        res = run_full_analysis(file.filename, file_bytes, job_description, job_title)
        
        # Save analysis entry to SQLite DB
        db_entry = Analysis(
            filename=res["filename"],
            candidate_name=res["candidate_name"],
            email=res["email"],
            phone=res["phone"],
            score=res["score"],
            completeness_score=res["completeness_score"],
            experience_level=res["experience_level"],
            summary=res["summary"],
            job_title=res["job_title"],
            job_description=res["job_description"],
            matching_skills=json.dumps(res["matching_skills"]),
            missing_skills=json.dumps(res["missing_skills"]),
            strengths=json.dumps(res["strengths"]),
            weaknesses=json.dumps(res["weaknesses"]),
            suggestions=json.dumps(res["suggestions"]),
            section_scores=json.dumps(res["section_scores"]),
            interview_questions=json.dumps(res["interview_questions"]),
            rewrite_suggestions=json.dumps(res["rewrite_suggestions"]),
            course_recommendations=json.dumps(res["course_recommendations"]),
            checklist=json.dumps(res["checklist"])
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)

        res["id"] = db_entry.id
        res["created_at"] = db_entry.created_at
        return res
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analysis failed: {str(e)}")


@router.get("/history", response_model=List[AnalysisListItem])
def get_history(db: Session = Depends(get_db)):
    """Fetch recent resume analysis records ordered by date."""
    records = db.query(Analysis).order_by(Analysis.created_at.desc()).all()
    return records


@router.get("/analysis/{id}", response_model=AnalysisResponse)
def get_analysis_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch single detailed analysis result by ID."""
    record = db.query(Analysis).filter(Analysis.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")

    # Deserialize JSON fields
    return {
        "id": record.id,
        "filename": record.filename,
        "candidate_name": record.candidate_name,
        "email": record.email,
        "phone": record.phone,
        "score": record.score,
        "completeness_score": record.completeness_score,
        "experience_level": record.experience_level,
        "summary": record.summary,
        "job_title": record.job_title,
        "job_description": record.job_description,
        "matching_skills": json.loads(record.matching_skills) if record.matching_skills else [],
        "missing_skills": json.loads(record.missing_skills) if record.missing_skills else [],
        "skill_categories": categorize_skills(json.loads(record.matching_skills) if record.matching_skills else []),
        "strengths": json.loads(record.strengths) if record.strengths else [],
        "weaknesses": json.loads(record.weaknesses) if record.weaknesses else [],
        "suggestions": json.loads(record.suggestions) if record.suggestions else [],
        "section_scores": json.loads(record.section_scores) if record.section_scores else {},
        "interview_questions": json.loads(record.interview_questions) if record.interview_questions else [],
        "rewrite_suggestions": json.loads(record.rewrite_suggestions) if record.rewrite_suggestions else [],
        "course_recommendations": json.loads(record.course_recommendations) if record.course_recommendations else [],
        "checklist": json.loads(record.checklist) if record.checklist else [],
        "created_at": record.created_at
    }


@router.delete("/analysis/{id}")
def delete_analysis(id: int, db: Session = Depends(get_db)):
    """Delete an analysis entry by ID."""
    record = db.query(Analysis).filter(Analysis.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")
    
    db.delete(record)
    db.commit()
    return {"message": "Analysis record deleted successfully.", "id": id}


@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Retrieve summary metrics for the Dashboard view."""
    records = db.query(Analysis).order_by(Analysis.created_at.desc()).all()
    
    total = len(records)
    if total == 0:
        return {
            "total_analyses": 0,
            "average_score": 0.0,
            "highest_score": 0,
            "recent_analyses": []
        }

    scores = [r.score for r in records]
    avg_score = round(sum(scores) / total, 1)
    max_score = max(scores)

    recent = [
        AnalysisListItem(
            id=r.id,
            filename=r.filename,
            candidate_name=r.candidate_name,
            score=r.score,
            experience_level=r.experience_level,
            job_title=r.job_title,
            created_at=r.created_at
        ) for r in records[:5]
    ]

    return {
        "total_analyses": total,
        "average_score": avg_score,
        "highest_score": max_score,
        "recent_analyses": recent
    }
