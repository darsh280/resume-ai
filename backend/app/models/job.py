from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_experience = Column(Float, default=0.0)
    extracted_skills = Column(Text, default="[]")       # JSON list stored as string
    required_qualifications = Column(Text, default="[]") # JSON list stored as string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
