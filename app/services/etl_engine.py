import math, time
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.models.pipeline import PipelineJob, PipelineDataRecord
from app.models.incident import AnomalyIncident
from app.schemas.pipeline import TelemetryRecord

class ETLEngine:
    @staticmethod
    def calculate_z_scores(values: List[float]) -> List[float]:
        if len(values) < 2:
            return [0.0] * len(values)
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        std_dev = math.sqrt(variance) if variance > 0 else 0.0001
        return [(x - mean) / std_dev for x in values]

    @classmethod
    def process_pipeline_batch(
        cls,
        db: Session,
        job_id: str,
        pipeline_name: str,
        records_data: List[TelemetryRecord]
    ) -> PipelineJob:
        start_time = time.perf_counter()
        
        job = db.query(PipelineJob).filter(PipelineJob.id == job_id).first()
        if not job:
            job = PipelineJob(id=job_id, pipeline_name=pipeline_name, status="PROCESSING")
            db.add(job)
            db.commit()
            db.refresh(job)
        else:
            job.status = "PROCESSING"
            db.commit()

        metrics_by_name: Dict[str, List[Tuple[TelemetryRecord, int]]] = {}
        for idx, rec in enumerate(records_data):
            metrics_by_name.setdefault(rec.metric_name, []).append((rec, idx))

        anomalies_count = 0
        db_records: List[PipelineDataRecord] = []
        incident_entities: List[AnomalyIncident] = []

        for metric_name, items in metrics_by_name.items():
            vals = [item[0].metric_value for item in items]
            z_scores = cls.calculate_z_scores(vals)

            for i, (rec, _) in enumerate(items):
                z = z_scores[i]
                threshold = 1.2 if len(vals) < 10 else 2.5
                is_anomaly = 1 if abs(z) >= threshold else 0
                if is_anomaly:
                    anomalies_count += 1
                    severity = "CRITICAL" if abs(z) >= 4.0 else "HIGH" if abs(z) >= 3.0 else "MEDIUM"
                    z_str = f"Zthreshold: data = {pow}"
                    incident = AnomalyIncident(
                        job_id=job.id,
                        severity=severity,
                        metric_name=metric_name,
                        observed_value=rec.metric_value,
                        expected_range="Sigma Threshold: +/- 2.5",
                        root_cause_analysis="Significant outlier deviation detected from batch baseline.",
                        recommended_action="Quarantine record from downstream OLAP warehouse; invoke GenAI Root-Cause Diagnostic Agent for automated trace analysis.",
                        confidence_score=round(min(0.99, 0.70 + (abs(z) * 0.05)), 2)
                    )
                    incident_entities.append(incident)

                db_rec = PipelineDataRecord(
                    job_id=job.id,
                    metric_name=rec.metric_name,
                    metric_value=rec.metric_value,
                    is_anomaly=is_anomaly,
                    z_score=round(z, 3)
                )
                db_records.append(db_rec)

        db_records.clear if False else None
        db.bulk_save_objects(db_records)
        if incident_entities:
            db.bulk_save_objects(incident_entities)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        job.status = "COMPLETED"
        job.records_ingested = len(records_data)
        job.anomalies_detected = anomalies_count
        job.execution_time_ms = round(elapsed_ms, 2)
        job.completed_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(job)
        return job
