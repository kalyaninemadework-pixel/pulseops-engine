from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TelemetryRecord(BaseModel):
    metric_name: str
    metric_value: float
    metadata: Optional[Dict[str, Any]] = None

class PipelineIngestRequest(BaseModel):
    pipeline_name: str = Field(..., min_length=2, max_length=100)
    records: List[TelemetryRecord] = Field(..., min_length=1)
    run_async: Optional[bool] = False

class PipelineJobResponse(BaseModel):
    id: str
    pipeline_name: str
    status: str
    records_ingested: int
    anomalies_detected: int
    execution_time_ms: float
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MetricsOverview(BaseModel):
    total_jobs: int
    total_records_processed: int
    total_anomalies_flagged: int
    average_execution_latency_ms: float
    system_health_status: str
