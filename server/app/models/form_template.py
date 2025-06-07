
import logging
import uuid

from datetime import datetime, timezone
from typing import Dict, Any

from sqlalchemy.orm import validates, relationship
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_continuum import make_versioned
from app.database import db
from app.models.constants.enums import FormStatus


logger = logging.getLogger(__name__)


make_versioned(user_cls='app.models.user.User')

class FormTemplate(db.Model):
    __versioned__ = {}
    __tablename__ = 'form_templates'

    id = mapped_column(db.Integer, primary_key=True)
    title = mapped_column(db.String(255), nullable=False)
    version = mapped_column(db.Integer, nullable=False, default=1)
    questions = mapped_column(db.Text, nullable=False)
    status = mapped_column(db.Enum(FormStatus), nullable=False, default=FormStatus.IN_PROCESS)
    practitioner_id = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_archived = mapped_column(db.Boolean, default=False, nullable=False)
    is_deleted = mapped_column(db.Boolean, default=False, nullable=False)

    created_at = mapped_column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    updated_at = mapped_column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )


    practitioner = relationship('User', back_populates='created_forms')

    assigned_forms = relationship(
        'AssignedForm',
        back_populates='form_template', 
        lazy='select' 
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
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'practitioner_name': getattr(self.practitioner, 'username', None)
        }

    def __repr__(self) -> str:
        return f'<FormTemplate {self.id} "{self.title}">'