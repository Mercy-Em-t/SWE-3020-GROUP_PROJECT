from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.audit import AuditLogResponse
from app.repositories.audit_repo import AuditRepository

router = APIRouter(prefix="/audit", tags=["Audit & Forensic Journal"])

@router.get("/logs", response_model=List[AuditLogResponse])
def get_audit_trail(limit: int = 50, db: Session = Depends(get_db)):
    return AuditRepository(db).get_recent_logs(limit=limit)
