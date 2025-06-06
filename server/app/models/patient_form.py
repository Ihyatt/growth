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
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )



    form_reviewer = db.relationship('User',backref='reviewed_forms', lazy=True)
    assigned_patient = db.relationship('User',backref='forms_as_patient', lazy=True)

    form_author = db.relationship('User',backref='forms_as_practitioner', lazy=True)



    @validates('form_data')
    def validate_form_data(self, key, form_data):
        if not form_data or len(form_data.strip()) == 0:
            raise ValueError("Form data cannot be empty")
        return form_data

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['submitted', 'reviewed', 'approved', 'rejected']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "practitioner_form_id": self.practitioner_form_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "reviewed_by": self.reviewed_by,
            "user_name": getattr(self.user, 'name', None),
            "reviewer_name": getattr(self.reviewer, 'name', None) if self.reviewer else None
        }

    def __repr__(self) -> str:
        return f"<UserForm id={self.id} user={self.patient_id} form={self.practitioner_form_id} status={self.status}>"