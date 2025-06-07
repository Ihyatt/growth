
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned
from app.database import db


logger = logging.getLogger(__name__)


make_versioned(user_cls='app.models.user.User')

class CareTeam(db.Model):
    __versioned__ = {}
    __tablename__ = 'care_teams'

    id = db.Column(db.Integer, primary_key=True)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    connected = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Many-to-one relationships (do NOT use lazy='dynamic' here)
    practitioner = relationship(
        "User",
        foreign_keys=[practitioner_id],
        backref=db.backref("care_team_practitioner", lazy="select"),
        lazy="joined"
    )
    patient = relationship(
        "User",
        foreign_keys=[patient_id],
        backref=db.backref("care_team_as_patient", lazy="select"),
        lazy="joined"
    )

    __table_args__ = (
        db.UniqueConstraint('patient_id', 'practitioner_id', name='_patient_practitioner_uc'),
    )

    def __repr__(self) -> str:
        return (
            f"<CareTeam(id={self.id}, "
            f"patient_id={self.patient_id}, "
            f"practitioner_id={self.practitioner_id}, "
            f"connected={self.connected})>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "practitioner_id": self.practitioner_id,
            "patient_data": self.patient.to_dict() if self.patient else None,
            "connected": self.connected,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }