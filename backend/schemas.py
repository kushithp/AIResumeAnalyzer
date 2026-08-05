from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    job_title: Optional[str] = "Target Job Role"
    job_description: str = Field(..., min_length=10, description="Job description text")


class AnalysisRequest(BaseModel):
    resume_text: str = Field(..., min_length=10, description="Extracted plain text of resume")
    filename: str = Field(..., description="Original filename of the resume")
    job_title: Optional[str] = "Target Role"
    job_description: str = Field(..., min_length=10, description="Job description text")


class SkillCategoryBreakdown(BaseModel):
    category: str
    skills: List[str]


class AnalysisResponse(BaseModel):
    id: Optional[int] = None
    filename: str
    candidate_name: Optional[str] = "Candidate"
    email: Optional[str] = None
    phone: Optional[str] = None
    score: int
    completeness_score: int
    experience_level: str
    summary: str
    job_title: Optional[str] = None
    job_description: str
    
    matching_skills: List[str] = []
    missing_skills: List[str] = []
    skill_categories: Optional[List[SkillCategoryBreakdown]] = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []
    section_scores: Dict[str, int] = {}
    interview_questions: List[str] = []
    rewrite_suggestions: List[Dict[str, str]] = []  # [{"original": ..., "suggested": ...}]
    course_recommendations: List[Dict[str, str]] = [] # [{"topic": ..., "reason": ...}]
    checklist: List[Dict[str, Any]] = [] # [{"item": ..., "passed": True/False}]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AnalysisListItem(BaseModel):
    id: int
    filename: str
    candidate_name: Optional[str] = "Candidate"
    score: int
    experience_level: str
    job_title: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_analyses: int
    average_score: float
    highest_score: int
    recent_analyses: List[AnalysisListItem]
