from datetime import datetime
from pydantic import BaseModel


class AuditLog(BaseModel):
    user: str
    role: str
    action: str
    resource: str
    status: str
    timestamp: datetime
    ip_address: str
