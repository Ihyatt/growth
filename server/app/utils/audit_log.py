import json
from flask import g
from app.database import db
from app.models.audit_log import AuditLog
from app.models.constants.enums import AuditActionType 

def log_audit(
    target_user_id: int,
    action_type: AuditActionType.APPROVED,
    details: dict = None
    ):
    admin_id = getattr(g, 'user_id', None)

    try:
        new_log = AuditLog(
            admin_id=admin_id,
            target_user_id=target_user_id,
            action_type=action_type,
            details=details
        )
        db.session.add(new_log)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback() 