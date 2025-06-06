
from datetime import datetime, timezone
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy import Column, ForeignKey, Boolean

from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db
from app.models.constants.enums import AuditActionStatus
from typing import Dict, Any

make_versioned(user_cls='app.models.user.User')

class AuditLog(db.Model):
    __versioned__ = {}
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    audited_user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    details = db.Column(JSONB, nullable=True)
    action_type = db.Column(Enum(AuditActionStatus), nullable=False)
    audited_model = db.Column(db.String(120), nullable=False)
    is_deleted = Column(Boolean, default=True, nullable=False)

    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    admin = relationship(
        'User',
        foreign_keys=[admin_id],
        backref=db.backref('admin_audit_logs', lazy='dynamic')
    )
    audited_user = relationship(
        'User',
        foreign_keys=[audited_user_id],
        backref=db.backref('user_audit_logs', lazy='dynamic')
    )

    @validates('audited_model')
    def validate_audited_model(self, key: str, model_name: str) -> str:
        if not model_name or not isinstance(model_name, str):
            raise ValueError("Model name must be a non-empty string")
        return model_name.lower()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "admin_email": getattr(self.admin, 'email', None),
            "audited_user_id": self.audited_user_id,
            "audited_user_email": getattr(self.audited_user, 'email', None),
            "action_type": self.action_type.value,
            "audited_model": self.audited_model,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return (
            f"<AuditLog id={self.id} "
            f"action_type={self.action_type.value} "
            f"admin_id={self.admin_id} "
            f"audited_user_id={self.audited_user_id}>"
        )