from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.incident import AnomalyIncident
from app.schemas.incident import AIDiagnosisRequest, AIDiagnosisResponse, IncidentResponse
from app.services.ai_agent import AutonomousRootCauseAgent

router = APIRouter(prefix="/agent", tags=["Autonomous GenAI Diagnostics"])

@router.post("/diagnose", response_model=AIDiagnosisResponse)
def run_autonomous_diagnosis(
    payload: AIDiagnosisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return AutonomousRootCauseAgent.diagnose_job_failure(
            db=db,
            job_id=payload.job_id,
            context_notes=payload.context_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/incidents", response_model=List[IncidentResponse])
def list_incident_reports(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(AnomalyIncident).order_by(AnomalyIncident.created_at.desc()).limit(limit).all()
