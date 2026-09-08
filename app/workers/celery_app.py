from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "pulseops_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="async_process_pipeline_task")
def async_process_pipeline_task(job_id: str, pipeline_name: str, records: list):
    from app.core.database import SessionLocal
    from app.services.etl_engine import ETLEngine
    from app.schemas.pipeline import TelemetryRecord
    
    db = SessionLocal()
    try:
        telemetry_records = [TelemetryRecord(**rec) for rec in records]
        job = ETLEngine.process_pipeline_batch(
            db=db,
            job_id=job_id,
            pipeline_name=pipeline_name,
            records_data=telemetry_records\n        )
        return {"status": "SUCCESS", "job_id": job.id, "records": job.records_ingested}
    finally:
        db.close()
