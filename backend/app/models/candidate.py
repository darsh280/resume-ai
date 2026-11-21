from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class CandidateRanking(Base):
    __tablename__ = "candidate_rankings"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    rank = Column(Integer, default=0)
    semantic_score = Column(Float, default=0.0)
    skill_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    education_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    matched_skills = Column(Text, default="[]")     # JSON
    missing_skills = Column(Text, default="[]")     # JSON
    additional_skills = Column(Text, default="[]")  # JSON
    recommendation = Column(String(50), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
