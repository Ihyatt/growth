import logging
import uuid

from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db
from app.models.constants.enums import AuditActionStatus
from typing import Dict, Any

logger = logging.getLogger(__name__)


make_versioned(user_cls='app.models.user.User') #tracks user that inserts/updates/deletes

class AuditLog(db.Model):
    __versioned__ = {} #creates historic record of update/insert/delete
    __tablename__ = 'audit_logs'

    id = mapped_column(db.Integer, primary_key=True)
    version = mapped_column(db.Integer, nullable=False, default=1)
    admin_id = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    audited_id = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    details = mapped_column(JSONB, nullable=True)
    action_type = mapped_column(db.Enum(AuditActionStatus), nullable=False, default=AuditActionStatus.SET_TO_PENDING )
    audited_model = mapped_column(db.String(120), nullable=False)
    is_deleted = mapped_column(db.Boolean, default=False, nullable=False)

    created_at = mapped_column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = mapped_column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    # Relationships: 'lazy="dynamic"' is invalid for many-to-one relationships
    admin = relationship(
        'User',
        foreign_keys=[admin_id],
        back_populates='audit_logs_as_admin',
        lazy='joined'
    )
    audited_user = relationship(
        'User',
        foreign_keys=[audited_id],
        back_populates='audit_logs_about_user',
        lazy='joined'
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
            "audited_id": self.audited_id,
            "audited_user_email": getattr(self.audited_user, 'email', None),
            "action_type": self.action_type.value if self.action_type else None,
            "audited_model": self.audited_model,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return (
            f"<AuditLog id={self.id} "
            f"action_type={self.action_type.value if self.action_type else None} "
            f"admin_id={self.admin_id} "
            f"audited_id={self.audited_id}>"
        )
    
