
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel
from sqlalchemy_continuum import make_versioned


make_versioned(user_cls=None)
class PractitionerForm(db.Model):
    __versioned__ = {}
    __tablename__ = 'practitioner_forms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    questions = db.Column(db.Text)
    responses = db.Column(db.Text)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # FK to User (practitioner)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))
