from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.model_enums import PermissionLevel, ValidationLevel


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    permission = db.Column(Enum(PermissionLevel), nullable=False, default=PermissionLevel.PATIENT)
    is_validated = db.Column(Enum(ValidationLevel), nullable=False, default=ValidationLevel.PENDING)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.permission == PermissionLevel.ADMIN
    
    @property
    def is_practitioner(self):
        return self.permission == PermissionLevel.PRACTITIONER

    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "permission": self.permission.value if self.permission else None,
            "is_validated": self.is_validated.value if self.is_validated else None,
            "is_active": 'ACTIVE' if self.is_active else 'INACTIVE',
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }