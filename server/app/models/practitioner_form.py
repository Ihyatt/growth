from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy import ForeignKey, Text, String, Column
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db


make_versioned(user_cls='app.models.user.User')


class PractitionerForm(db.Model):
    __versioned__ = {}
    __tablename__ = 'practitioner_forms'

    id = Column(db.Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    questions = Column(Text, nullable=False)
    responses = Column(Text)
    is_active = Column(db.Boolean, default=True, nullable=False) 
    practitioner_id = Column(db.Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now()) 
    updated_at = Column(
        db.DateTime, 
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    practitioner = relationship('User', back_populates='created_forms')
    report_comments = relationship('ReportComment', back_populates='form', cascade='all, delete-orphan')


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
            'description': self.description,
            'is_active': self.is_active,
            'practitioner_id': self.practitioner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'practitioner_name': getattr(self.practitioner, 'name', None)
        }

    def __repr__(self) -> str:
        return f'<PractitionerForm {self.id} "{self.title}">'
