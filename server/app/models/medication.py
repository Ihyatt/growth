from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel


from sqlalchemy_continuum import make_versioned


make_versioned(user_cls=None)
class Medication(db.Model):
    __versioned__ = {}
    __tablename__ = 'medications'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    dosage = db.Column(db.String)
    instructions = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

make_versioned(user_cls=None)
class MedicationComment(db.Model):
    __versioned__ = {}
    __tablename__ = 'medication_comments'
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'))
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)