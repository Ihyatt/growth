from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel


class PractitionerForm(db.Model):
    __tablename__ = 'practitioner_forms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    questions = db.Column(db.Text)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # FK to User (practitioner)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responses = db.Column(Enum(PermissionLevel), nullable=False, default=PermissionLevel.PATIENT)
    practitioner = relationship("User", backref="practitioner_forms", foreign_keys=[practitioner_id])
