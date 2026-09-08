from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.pipeline import PipelineJob
from app.schemas.pipeline import MetricsOverview

router = APIRouter(prefix="/analytics", tags=["System Analytics & Telemetry"])

@router.get("/overview", response_model=MetricsOverview)
def get_system_metrics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_jobs = db.query(PipelineJob).count()
    total_records = db.query(func.sum(PipelineJob.records_ingested)).scalar() or 0
    total_anomalies = db.query(func.sum(PipelineJob.anomalies_detected)).scalar() or 0
    avg_latency = db.query(func.avg(PipelineJob.execution_time_ms)).scalar() or 0.0

    health = "OPTIMAL" if (total_anomalies / max(1, total_records)) < 0.05 else "WARNING"

    return MetricsOverview(
        total_jobs=total_jobs,
        total_records_processed=int(total_records),
        total_anomalies_flagged=int(total_anomalies),
        average_execution_latency_ms=round(float(avg_latency), 2),
        system_health_status=health
    )
