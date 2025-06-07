
import logging
from datetime import datetime, timezone
from typing import Dict, Any

from sqlalchemy.orm import validates, relationship # Import relationship here

from sqlalchemy_continuum import make_versioned
from app.database import db
from app.models.constants.enums import FormStatus # Ensure this enum is correctly defined


logger = logging.getLogger(__name__)


make_versioned(user_cls='app.models.user.User') # Keep user_cls if you're consistently using app.models.user.User

class FormTemplate(db.Model):
    __versioned__ = {}
    __tablename__ = 'form_templates'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    # Changed to JSONB for better handling of structured questions
    # If questions is truly just text, Text is fine, but if it implies structure (e.g., list of dicts), JSONB is better.
    # Assuming questions are stored as a JSON string representing a list of question objects.
    questions = db.Column(db.Text, nullable=False) # Keep as Text if it's just raw text/markdown. If structured, use JSONB.
    status = db.Column(db.Enum(FormStatus), nullable=False, default=FormStatus.IN_PROCESS)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False) # Use timezone=True for UTC
    updated_at = db.Column(
        db.DateTime(timezone=True), # Use timezone=True for UTC
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    # Relationships
    # Corrected 'back_populates' to match 'created_forms' on the User model
    practitioner = relationship('User', back_populates='created_forms')

    # This relationship should be from FormTemplate to FormAssignment (plural is common)
    # The 'back_populates' should point to the correct attribute on the 'AssignedForm' model.
    # Assuming 'AssignedForm' has a relationship back to 'FormTemplate' called 'form_template'
    assigned_forms = relationship(
        'AssignedForm',
        back_populates='form_template', # This should be the name of the relationship on AssignedForm pointing back to FormTemplate
        lazy='select' # 'select' (default) or 'joined' or 'dynamic' depending on loading strategy
    )

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
            'is_deleted': self.is_deleted, # Added missing is_deleted field
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'practitioner_name': getattr(self.practitioner, 'username', None) # Safely get username
        }

    def __repr__(self) -> str:
        return f'<FormTemplate {self.id} "{self.title}">'