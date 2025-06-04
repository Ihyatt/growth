from datetime import datetime, timezone
from app.database import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.models.model_enums import AuditActionType 

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    target_user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    action_type = db.Column(Enum(AuditActionType), nullable=False)
    description = db.Column(db.String(256))

    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    admin = relationship("User", foreign_keys=[admin_id], backref="admin_logs")
    target_user = relationship("User", foreign_keys=[target_user_id], backref="user_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "admin_email": self.admin.email if self.admin else None,
            "target_user_id": self.target_user_id,
            "target_user_email": self.target_user.email if self.target_user else None,
            "action_type": self.action_type.value,
            "description": self.description,
            "timestamp": self.timestamp.isoformat()
        }