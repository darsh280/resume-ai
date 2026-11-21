from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    file_path = Column(String(500))
    file_type = Column(String(10))
    candidate_name = Column(String(255), default="")
    email = Column(String(255), default="")
    phone = Column(String(50), default="")
    raw_text = Column(Text, default="")
    extracted_skills = Column(Text, default="[]")   # JSON
    education = Column(Text, default="[]")           # JSON
    work_experience = Column(Text, default="[]")     # JSON
    projects = Column(Text, default="[]")            # JSON
    certifications = Column(Text, default="[]")      # JSON
    years_experience = Column(Float, default=0.0)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    job_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=True)
