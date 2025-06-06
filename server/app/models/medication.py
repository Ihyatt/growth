from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import ForeignKey, String, Text, Column
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db

make_versioned(user_cls='app.models.user.User')

class Medication(db.Model):
    __versioned__ = {}
    __tablename__ = 'medications'

    id = Column(db.Integer, primary_key=True)
    patient_id = Column(db.Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(120), nullable=False)
    dosage = Column(String(120), nullable=False)
    practioner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    frequency = Column(String(120))
    start_date = Column(db.Date)
    end_date = Column(db.Date)
    instructions = Column(Text)
    is_active = Column(db.Boolean, default=True, nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now())
    updated_at = Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    patient = relationship('User', back_populates='medications')
    comments = relationship('MedicationComment', back_populates='medication', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Medication name cannot be empty")
        return name.strip()

    @validates('dosage')
    def validate_dosage(self, key, dosage):
        if not dosage or len(dosage.strip()) == 0:
            raise ValueError("Dosage cannot be empty")
        return dosage.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'instructions': self.instructions,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f'<Medication {self.id} {self.name} for patient {self.patient_id}>'
