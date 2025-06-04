

from datetime import datetime, timezone
from app.database import db
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned


make_versioned(user_cls=None)
class Follow(db.Model):
    __versioned__ = {}
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
