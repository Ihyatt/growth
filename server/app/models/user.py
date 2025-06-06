from datetime import datetime
from typing import Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum, String, Column, Boolean
from sqlalchemy.orm import validates
from sqlalchemy_continuum import make_versioned
from sqlalchemy.orm import relationship, validates
from app.database import db
from app.models.report import Report
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


    medications = db.relationship('Medication', backref='patient_owner', lazy=True)
    medications_comments = db.relationship('Comment', backref='medication_comment_author', lazy=True)
    report_comments = db.relationship('Comment', backref='report_comment_author', lazy=True)
    
    audit_logs_as_admin = db.relationship('Audit_Log', backref='admin', lazy=True)
    audit_logs_about_user = db.relationship('Audit_Log', backref='audited_user', lazy=True)
    
    forms_as_patient = db.relationship('Patient_Form', backref='assigned_patient', lazy=True)
    forms_as_practitioner = db.relationship('Practitioner_Form', backref='form_author', lazy=True)

    reports_as_patient = db.relationship('Report',backref='reported_patient', lazy=True)
    reports_as_practitioner = db.relationship('Report', backref='report_reviewer',lazy=True)

    follow_as_patient = db.relationship('Follow', backref='followed', lazy=True)
    follow_as_practitioner = db.relationship('Follow', backref='follower',lazy=True)


    def set_password(self, password: str) -> None:
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self) -> bool:
        return self.user_level == UserLevel.ADMIN

    @property
    def is_practitioner(self) -> bool:
        return self.user_level == UserLevel.PRACTITIONER

    @property
    def is_patient(self) -> bool:
        return self.user_level == UserLevel.PATIENT

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "username": self.username,
            "user_level": self.user_level.value,
            "full_name": self.full_name,
        }

        return data

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} user_level={self.user_level}>"
    