
from typing import Dict, Any
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db

make_versioned(user_cls='app.models.user.User')

class Medication(db.Model):
    __versioned__ = {}
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(120), nullable=False)
    practioner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    frequency = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    instructions = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    patient_owner = relationship('User', back_populates='medications')
    medication_comments = relationship('MedicationComment', back_populates='medication')

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


make_versioned(user_cls='app.models.user.User')

class MedicationComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    
    medication_comment_author = db.relationship('User', backref=db.backref('medications_comments', lazy=True))
    medication = db.relationship('Medication', back_populates='medication_comments', lazy=True)


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
        
        return data
