from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned
from app.database import db


make_versioned(user_cls='app.models.user.User')

class Follow(db.Model):
    __versioned__ = {}
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    connected = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )


    follower = relationship( "User", back_populates = "follow_as_practitioner", lazy=True)
    followed = relationship("User",  back_populates="follow_as_patient", lazy=True)


    __table_args__ = (
        db.UniqueConstraint('patient_id', 'practitioner_id', name='_patient_practitioner_uc'),
    )

    def __repr__(self) -> str:
        return (
            f"<Follow(id={self.id}, "
            f"patient_id={self.patient_id}, "
            f"practitioner_id={self.practitioner_id}, "
            f"status={self.status})>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "practitioner_id": self.practitioner_id,
            "patient_id": self.patient_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }