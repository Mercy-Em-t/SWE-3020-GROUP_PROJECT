from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor_email: str
    action: str
    entity_name: str
    entity_id: Optional[int]
    delta: Optional[str]
    ip_address: str
    timestamp: datetime
