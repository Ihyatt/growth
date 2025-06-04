import json

from app.models.audit_log import AuditLog


def log_audit(audited_user_id, action_type, details, model):
    try:
        AuditLog(
            admin_id=g.user_id,
            audited_user_id = audited_user_id,
            details = json.dumps(details), 
            action_type = action_type,
            audited_model = model
        )
        db.session.commit()
        # log success
    except:
        # log failure
        pass