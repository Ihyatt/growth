
import logging
from datetime import datetime
from typing import Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship # relationship is already imported, good.
from sqlalchemy_continuum import make_versioned
from app.database import db
from app.models.constants.enums import UserLevel, UserApprovalStatus, ProfileStatus # Ensure these enums are correctly defined


logger = logging.getLogger(__name__)



make_versioned(user_cls='app.models.user.User') # Keep user_cls

class User(db.Model):
    __tablename__ = 'users'
    __versioned__ = {}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    user_level = db.Column(db.Enum(UserLevel), nullable=False, default=UserLevel.PATIENT)
    approval_status = db.Column(db.Enum(UserApprovalStatus), nullable=False, default=UserApprovalStatus.PENDING)
    profile_status = db.Column(db.Enum(ProfileStatus), nullable=False, default=ProfileStatus.ACTIVE)

    last_login_at = db.Column(db.DateTime(timezone=True)) # Use timezone=True
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False) # Use timezone=True
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now(), nullable=False) # Use timezone=True
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships - updated to match common back_populates patterns
    # IMPORTANT: The 'back_populates' values MUST match the names of the
    # relationship attributes defined on the *other* model.

    medications = relationship('Medication', back_populates='patient_owner', lazy='dynamic') # Use dynamic for collections
    medication_comments = relationship('MedicationComment', back_populates='medication_comment_author', lazy='dynamic')
    report_comments = relationship('ReportComment', back_populates='report_comment_author', lazy='dynamic')

    audit_logs_as_admin = relationship('AuditLog', back_populates='admin', lazy='dynamic')
    audit_logs_about_user = relationship('AuditLog', back_populates='audited_user', lazy='dynamic')

    forms_as_patient = relationship('AssignedForm', back_populates='assigned_patient', lazy='dynamic')
    reviewed_forms = relationship('AssignedForm', back_populates='form_reviewer', lazy='dynamic')

    # Corrected back_populates to 'practitioner' as defined on FormTemplate
    created_forms = relationship('FormTemplate', back_populates='practitioner', lazy='dynamic')

    reports_as_patient = relationship('Report', back_populates='reported_patient', lazy='dynamic')
    reports_as_practitioner = relationship('Report', back_populates='report_reviewer', lazy='dynamic')

    # Fixed typo: care_team_as_practitioner (was care_taem_as_practitioner)
    # Ensure back_populates names match what's on the CareTeam model
    care_team_as_patient = relationship('CareTeam', back_populates='patient_cared_for', lazy='dynamic')
    care_team_as_practitioner = relationship('CareTeam', back_populates='practitioner_caring_for', lazy='dynamic')


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
        return self.username or ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email, # Added email for completeness in dict
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_level": getattr(self.user_level, 'value', None),
            "approval_status": getattr(self.approval_status, 'value', None), # Added for completeness
            "profile_status": getattr(self.profile_status, 'value', None), # Added for completeness
            "full_name": self.full_name,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted, # Added for completeness
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} user_level={self.user_level}>"