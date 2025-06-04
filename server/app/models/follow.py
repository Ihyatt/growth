

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel



class Follow(db.Model):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True)
    practitioner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))

    follower = relationship("User", foreign_keys=[follower_id], backref="patients_following")

    followed = relationship("User", foreign_keys=[followed_id], backref="practitioners")

    __table_args__ = (UniqueConstraint('patient_id', 'practitioner_id', name='_practitioner_follow_uc'),)

    def __repr__(self):
        return f"<Follow(patient_id={self.patient_id}, practitioner_id={self.practitioner_id})>"
