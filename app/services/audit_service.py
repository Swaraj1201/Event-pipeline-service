from datetime import datetime

from app.db.database import get_database


def log_audit_event(
    user: str,
    role: str,
    action: str,
    resource: str,
    status: str,
    ip_address: str
):
    """
    Log an audit event to MongoDB.
    
    Args:
        user: Username who performed the action
        role: User's role
        action: Action performed (e.g., "create", "read", "update", "delete")
        resource: Resource that was accessed (e.g., "/events", "/auth/login")
        status: Status of the action (e.g., "success", "failure")
        ip_address: IP address of the client
    """
    db = get_database()
    
    audit_entry = {
        "user": user,
        "role": role,
        "action": action,
        "resource": resource,
        "status": status,
        "timestamp": datetime.utcnow(),
        "ip_address": ip_address
    }
    
    db.audit_logs.insert_one(audit_entry)
