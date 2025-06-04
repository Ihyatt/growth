
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel

class UserForm(db.Model):
    __tablename__ = 'user_forms'

    id = db.Column(db.Integer, primary_key=True)
    sbumitted_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    form_data = db.Column(db.Text, nullable=False)
    practitioner_form_id = db.Column(db.Integer, db.ForeignKey('practitioner_forms.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))

    user = relationship("User", backref="user_forms", foreign_keys=[user_id])

    def __repr__(self):
        return f"<FormSubmission {self.id} for Form {self.practitioner_form_id}>"