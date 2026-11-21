from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    name = Column(String(255), default="")
    total_resumes = Column(Integer, default=0)
    avg_score = Column(Float, default=0.0)
    top_candidate = Column(String(255), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
