from typing import Dict, Any
from sqlalchemy import ForeignKey, Text, String, Column, Enum
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db
from sqlalchemy_continuum import make_versioned


make_versioned(user_cls='app.models.user.User')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False) #('medication', 'report')
    resource_id = db.Column(db.Integer, nullable=False) #(e.g., medication.id, report.id)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    is_deleted = Column(Boolean, default=True, nullable=False)

    created_at = Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f'<Comment {self.id} on {self.resource_type}:{self.resource_id}>'

    def to_dict(self, include_user=True):
        data = {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
        }
        if include_user and self.user:
            data["user"] = {"id": self.user.id, "username": self.user.username}
        return data
