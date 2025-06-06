from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned
from app.database import db


make_versioned(user_cls='app.models.user.User')

class Follow(db.Model):
    __versioned__ = {}
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True)
    practitioner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    practitioner = relationship(
        "User",
        foreign_keys=[practitioner_id],
        backref=db.backref("patients_following", lazy='dynamic')
    )
    patient = relationship(
        "User",
        foreign_keys=[patient_id],
        backref=db.backref("practitioners_followed", lazy='dynamic')
    )

    __table_args__ = (
        UniqueConstraint('patient_id', 'practitioner_id', name='_patient_practitioner_uc'),
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