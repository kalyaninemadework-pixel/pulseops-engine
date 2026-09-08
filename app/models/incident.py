from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class AnomalyIncident(Base):
    __tablename__ = "anomaly_incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    job_id = Column(String(36), ForeignKey("pipeline_jobs.id"), index=True, nullable=False)
    severity = Column(String(20), default="MEDIUM", index=True, nullable=False)
    metric_name = Column(String(100), nullable=False)
    observed_value = Column(Float, nullable=False)
    expected_range = Column(String(100), nullable=False)
    root_cause_analysis = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.95, nullable=False)
    resolved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    job = relationship("PipelineJob", back_populates="incidents")
