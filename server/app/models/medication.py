
import logging
from typing import Dict, Any
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db


logger = logging.getLogger(__name__)


make_versioned(user_cls='app.models.user.User')


class Medication(db.Model):
    __versioned__ = {}
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(120), nullable=False)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ✅ fixed typo in "practioner_id"
    frequency = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    instructions = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    patient_owner = relationship('User', foreign_keys=[patient_id], backref='medications', lazy='select')
    practitioner = relationship('User', foreign_keys=[practitioner_id], backref='prescribed_medications', lazy='select')
    medication_comments = relationship('MedicationComment', back_populates='medication', cascade="all, delete-orphan")

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

# Only needed once per module
# make_versioned(...) is already called above — removed duplicate here

class MedicationComment(db.Model):
    __tablename__ = 'medication_comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)  # ✅ fixed table name
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ✅ fixed table name

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    medication_comment_author = relationship('User', backref='medications_comments', lazy='select')
    medication = relationship('Medication', back_populates='medication_comments', lazy='select')

    def __repr__(self):
        return f'<MedicationComment {self.id} on Medication:{self.medication_id}>'

    def to_dict(self, include_user=True):
        data = {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "medication_id": self.medication_id,
            "user_id": self.user_id
        }
        if include_user:
            data["user_email"] = getattr(self.medication_comment_author, "email", None)
        return data