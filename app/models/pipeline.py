from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class PipelineJob(Base):
    __tablename__ = "pipeline_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    pipeline_name = Column(String(100), index=True, nullable=False)
    status = Column(String(50), default="PENDING", index=True, nullable=False)
    records_ingested = Column(Integer, default=0, nullable=False)
    anomalies_detected = Column(Integer, default=0, nullable=False)
    execution_time_ms = Column(Float, default=0.0, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    records = relationship("PipelineDataRecord", back_populates="job", cascade="all, delete-orphan")
    incidents = relationship("AnomalyIncident", back_populates="job", cascade="all, delete-orphan")

class PipelineDataRecord(Base):
    __tablename__ = "pipeline_data_records"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(36), ForeignKey("pipeline_jobs.id"), index=True, nullable=False)
    metric_name = Column(String(100), index=True, nullable=False)
    metric_value = Column(Float, nullable=False)
    is_anomaly = Column(Integer, default=0, index=True, nullable=False)
    z_score = Column(Float, default=0.0, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    job = relationship("PipelineJob", back_populates="records")
