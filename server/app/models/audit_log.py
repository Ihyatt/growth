

from sqlalchemy import Enum, ForeignKey
from app.models.constants.enums import AuditActionType
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned
from app.database import db


make_versioned(user_cls=None)

class AuditLog(db.Model):
    __versioned__ = {}
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    audited_user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    details = db.Column(JSON, nullable=True)
    action_type = db.Column(Enum(AuditActionType), nullable=False)
    audited_model = db.Column(db.String(120), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))


    admin = relationship('User', foreign_keys=[admin_id], backref='admin_audit_logs')
    audited_user = relationship('User', foreign_keys=[audited_user_id], backref='audited_logs')

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "admin_email": self.admin.email if self.admin else None,
            "audited_user": self.audited_user,
            "target_user_email": self.audited_user_id.email if self.audited_user_id else None,
            "action_type": self.action_type.value,
            "timestamp": self.timestamp.isoformat()
        }