
from sqlalchemy import Enum, ForeignKey
from app.models.constants.enums import AuditActionType, PermissionLevel
from datetime import datetime, timezone
from app.database import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    audited_user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    details = db.Column(JSON, nullable=True)
    action_type = db.Column(Enum(AuditActionType), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))


    admin = relationship('User', foreign_keys=[admin_id], backref='admin_audit_logs')
    audited_user = relationship('User', foreign_keys=[target_user_id], backref='audited_logs')

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "admin_email": self.admin.email if self.admin else None,
            "target_user_id": self.target_user_id,
            "target_user_email": self.audited_user_id.email if self.audited_user_id else None,
            "action_type": self.action_type.value,
            "timestamp": self.timestamp.isoformat()
        }