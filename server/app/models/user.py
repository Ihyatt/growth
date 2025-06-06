from datetime import datetime
from typing import Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum, String, Column, Boolean
from sqlalchemy.orm import validates
from sqlalchemy_continuum import make_versioned
from app.database import db
from app.models.constants.enums import UserLevel, ApprovalStatus, ProfileStatus


make_versioned(user_cls='app.models.user.User')

class User(db.Model):

    __tablename__ = 'users'
    __versioned__ = {}

    id = Column(db.Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(512), nullable=False)
    first_name = Column(String(80))
    last_name = Column(String(80))
    
    user_level = Column(Enum(UserLevel), nullable=False, default=UserLevel.PATIENT)
    approval_status = Column(Enum(ApprovalStatus), nullable=False, default=ApprovalStatus.PENDING)
    profile_status = Column(Enum(ProfileStatus), nullable=False, default=ProfileStatus.ACTIVE)

    last_login_at = Column(db.DateTime)
    created_at = Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def set_password(self, password: str) -> None:
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.permission == UserLevel.ADMIN

    @property
    def is_practitioner(self) -> bool:
        return self.permission == UserLevel.PRACTITIONER

    @property
    def is_patient(self) -> bool:
        return self.permission == UserLevel.PATIENT

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @validates('email')
    def validate_email(self, key: str, email: str) -> str:
        if '@' not in email:
            raise ValueError("Invalid email address")
        return email.lower()

    @validates('username')
    def validate_username(self, key: str, username: str) -> str:
        if len(username) < 4:
            raise ValueError("Username must be at least 4 characters")
        return username

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "username": self.username,
            "user_level": self.user_level.value,
            "validation_status": self.validation_status.value,
            "approval_status": self.approval_status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "full_name": self.full_name,
        }
        if include_sensitive:
            data["email"] = self.email
            data["last_login_at"] = self.last_login_at.isoformat() if self.last_login_at else None
        return data

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} permission={self.permission.name}>"
    