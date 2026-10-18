from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from database import Base


class Analysis(Base):
    """SQLAlchemy ORM Model representing a stored Resume Analysis record."""

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    candidate_name = Column(String(150), nullable=True)
    email = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=True)
    score = Column(Integer, nullable=False, default=0)
    completeness_score = Column(Integer, nullable=False, default=0)
    experience_level = Column(String(50), nullable=False, default="Junior")
    summary = Column(Text, nullable=True)
    job_title = Column(String(200), nullable=True)
    job_description = Column(Text, nullable=False)
    
    # Structured JSON data fields stored as JSON strings
    matching_skills = Column(Text, nullable=True)  # JSON list
    missing_skills = Column(Text, nullable=True)   # JSON list
    strengths = Column(Text, nullable=True)        # JSON list
    weaknesses = Column(Text, nullable=True)       # JSON list
    suggestions = Column(Text, nullable=True)      # JSON list
    section_scores = Column(Text, nullable=True)   # JSON dict
    interview_questions = Column(Text, nullable=True) # JSON list
    rewrite_suggestions = Column(Text, nullable=True) # JSON list
    course_recommendations = Column(Text, nullable=True) # JSON list
    checklist = Column(Text, nullable=True)        # JSON list
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
