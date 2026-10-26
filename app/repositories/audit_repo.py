from typing import List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.entities import AuditLog

class AuditRepository(BaseRepository[AuditLog]):
    def __init__(self, db: Session):
        super().__init__(AuditLog, db)

    def log_event(
        self,
        actor_email: str,
        action: str,
        entity_name: str,
        entity_id: int = None,
        delta: str = None,
        ip_address: str = "127.0.0.1"
    ) -> AuditLog:
        entry = AuditLog(
            actor_email=actor_email,
            action=action,
            entity_name=entity_name,
            entity_id=entity_id,
            delta=delta,
            ip_address=ip_address
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_recent_logs(self, limit: int = 50) -> List[AuditLog]:
        return self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
