from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class IncidentResponse(BaseModel):
    id: str
    job_id: str
    severity: str
    metric_name: str
    observed_value: float
    expected_range: str
    root_cause_analysis: str
    recommended_action: str
    confidence_score: float
    resolved: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AIDiagnosisRequest(BaseModel):
    job_id: str
    context_notes: Optional[str] = None

class AIDiagnosisResponse(BaseModel):
    incident_id: str
    job_id: str
    severity: str
    metric_name: str
    root_cause_summary: str
    detailed_explanation: str
    automated_remediation_plan: str
    confidence_score: float
    status: str
