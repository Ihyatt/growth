from datetime import datetime
from typing import Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
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

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    
    user_level = db.Column(db.Enum(UserLevel), nullable=False, default=UserLevel.PATIENT)
    approval_status = db.Column(db.Enum(ApprovalStatus), nullable=False, default=ApprovalStatus.PENDING)
    profile_status = db.Column(db.Enum(ProfileStatus), nullable=False, default=ProfileStatus.ACTIVE)

    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)


    medications = db.relationship('Medication', back_populates='patient_owner', lazy=True)
    medications_comments = db.relationship('Comment', back_populates='medication_comment_author', lazy=True)
    report_comments = db.relationship('Comment', back_populates='report_comment_author', lazy=True)
    
    audit_logs_as_admin = db.relationship('Audit_Log', back_populates='admin', lazy=True)
    audit_logs_about_user = db.relationship('Audit_Log', back_populates='audited_user', lazy=True)
    
    forms_as_patient = db.relationship('Patient_Form', back_populates='assigned_patient', lazy=True)
    reviewed_forms = db.relationship('Patient_Form', back_populates='form_reviewer', lazy=True)

    forms_as_practitioner = db.relationship('Practitioner_Form', back_populates='form_author', lazy=True)
    

    reports_as_patient = db.relationship('Report',back_populates='reported_patient', lazy=True)
    reports_as_practitioner = db.relationship('Report', back_populates='report_reviewer',lazy=True)

    follow_as_patient = db.relationship('Follow', back_populates='followed', lazy=True)
    follow_as_practitioner = db.relationship('Follow', back_populates='follower',lazy=True)


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
    