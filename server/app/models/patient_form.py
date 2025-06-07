from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned

from app.database import db
from app.models.constants.enums import FormStatus

make_versioned(user_cls='app.models.user.User')


class PatientForm(db.Model):
    __versioned__ = {}
    __tablename__ = 'user_forms'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    form_data = db.Column(db.Text, nullable=False)
    practitioner_form_id = db.Column(db.Integer, db.ForeignKey('practitioner_forms.id'), nullable=False)
    status = db.Column(db.Enum(FormStatus), nullable=False, default=FormStatus.TODO)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    # Relationships
    assigned_patient = relationship('User', foreign_keys=[patient_id], backref='forms_as_patient', lazy='select')
    form_reviewer = relationship('User', foreign_keys=[reviewed_by_id], backref='reviewed_forms', lazy='select')

    # You may need a separate table/model for practitioner forms; below assumes it's another User
    # form_author = relationship('User', foreign_keys=[practitioner_form_id], backref='forms_as_practitioner', lazy='select')

    practitioner_form = relationship('PractitionerForm', backref='patient_forms', lazy='select')

    @validates('form_data')
    def validate_form_data(self, key, form_data):
        if not form_data or len(form_data.strip()) == 0:
            raise ValueError("Form data cannot be empty")
        return form_data.strip()

    @validates('status')
    def validate_status(self, key, status):
        if isinstance(status, str):
            status = FormStatus[status.upper()] if status.upper() in FormStatus.__members__ else None
        if not isinstance(status, FormStatus):
            raise ValueError(f"Invalid status. Must be one of: {[s.name for s in FormStatus]}")
        return status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "practitioner_form_id": self.practitioner_form_id,
            "status": self.status.name if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "reviewed_by": self.reviewed_by_id,
            "patient_name": getattr(self.assigned_patient, 'name', None),
            "reviewer_name": getattr(self.form_reviewer, 'name', None)
        }

    def __repr__(self) -> str:
        return f"<PatientForm id={self.id} patient={self.patient_id} form={self.practitioner_form_id} status={self.status.name if self.status else None}>"