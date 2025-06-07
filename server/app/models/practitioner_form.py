from datetime import datetime, timezone
from typing import Dict, Any

from sqlalchemy.orm import validates

from sqlalchemy_continuum import make_versioned
from app.database import db 
from app.models.constants.enums import FormStatus

make_versioned(user_cls='app.models.user.User')

class PractitionerForm(db.Model):
    __versioned__ = {}
    __tablename__ = 'practitioner_forms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    questions = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(FormStatus), nullable=False, default=FormStatus.IN_PROCESS)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_archived = db.Column(db.Boolean, default=False, nullable=False)  # Usually default False for archived flags
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    # Relationships
    practitioner = db.relationship('User', back_populates='created_forms')

    # Fix relationship name to match PatientForm table and attribute
    forms_as_practitioner = db.relationship('PatientForm', back_populates='practitioner_form', lazy='select')

    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters long")
        return title.strip()

    @validates('questions')
    def validate_questions(self, key, questions):
        if not questions or len(questions.strip()) == 0:
            raise ValueError("Questions cannot be empty")
        return questions.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status.name if self.status else None,
            'practitioner_id': self.practitioner_id,
            'is_archived': self.is_archived,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'practitioner_name': getattr(self.practitioner, 'username', None)
        }

    def __repr__(self) -> str:
        return f'<PractitionerForm {self.id} "{self.title}">'