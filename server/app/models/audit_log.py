
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    target_user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    action_type = db.Column(Enum(AuditActionType), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))


    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "admin_email": self.admin.email if self.admin else None,
            "target_user_id": self.target_user_id,
            "target_user_email": self.target_user.email if self.target_user else None,
            "action_type": self.action_type.value,
            "timestamp": self.timestamp.isoformat()
        }