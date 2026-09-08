import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.pipeline import PipelineJob
from app.schemas.pipeline import PipelineIngestRequest, PipelineJobResponse
from app.services.etl_engine import ETLEngine

router = APIRouter(prefix="/pipelines", tags=["Data Ingestion & Pipelines"])

@router.post("/ingest", response_model=PipelineJobResponse, status_code=status.HTTP_202_ACCEPTED)
def ingest_telemetry_batch(
    payload: PipelineIngestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job_id = str(uuid.uuid4())
    
    if payload.run_async:
        try:
            from app.workers.celery_app import async_process_pipeline_task
            record_dicts = [rec.model_dump() for rec in payload.records]
            async_process_pipeline_task.delay(job_id, payload.pipeline_name, record_dicts)
            job = PipelineJob(id=job_id, pipeline_name=payload.pipeline_name, status="PROCESSING", records_ingested=len(payload.records))
            db.add(job)
            db.commit()
            db.refresh(job)
            return job
        except Exception:
            pass

    job = ETLEngine.process_pipeline_batch(
        db=db,
        job_id=job_id,
        pipeline_name=payload.pipeline_name,
        records_data=payload.records
    )
    return job

@router.get("/jobs", response_model=List[PipelineJobResponse])
def list_pipeline_jobs(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(PipelineJob)
    if status_filter:
        query = query.filter(PipelineJob.status == status_filter.upper())
    return query.order_by(PipelineJob.created_at.desc()).offset(offset).limit(limit).all()

@router.get("/jobs/{job_id}", response_model=PipelineJobResponse)
def get_pipeline_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(PipelineJob).filter(PipelineJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job '{job_id}' not found.")
    return job
