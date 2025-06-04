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
    timestamp = Column(DateTime, server_default=func.now()) # When the follow occurred

    follower = relationship("User", foreign_keys=[follower_id], backref="patients_following")

    followed = relationship("User", foreign_keys=[followed_id], backref="practitioners")

    __table_args__ = (UniqueConstraint('follower_id', 'followed_id', name='_user_follow_uc'),)

    def __repr__(self):
        return f"<Follow(follower_id={self.follower_id}, followed_id={self.followed_id})>"
