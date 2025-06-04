from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel

class UserForm(db.Model):
    __tablename__ = 'user_forms'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    form_data = db.Column(db.Text, nullable=False)
    practitioner_form_id = db.Column(db.Integer, db.ForeignKey('practitioner_forms.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship("User", backref="user_forms", foreign_keys=[user_id])
