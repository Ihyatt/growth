from typing import Dict, Any
from sqlalchemy import ForeignKey, Text, String, Column, Enum, Boolean
from sqlalchemy.orm import relationship, validates
from sqlalchemy_continuum import make_versioned
from app.database import db

make_versioned(user_cls='app.models.user.User')

class Report(db.Model):
    __versioned__ = {}
    __tablename__ = 'reports'

    id = Column(db.Integer, primary_key=True)
    report_name = Column(String(255), nullable=False)
    report_data = Column(Text, nullable=False)
    file_format = Column(String(10), default='json')
    patient_id = Column(db.Integer, ForeignKey('users.id'))
    patient_username = Column(String(80), unique=True, nullable=False)
    practitioner_id = Column(db.Integer, ForeignKey('users.id'))
    is_deleted = Column(Boolean, default=True, nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    generator = relationship('User', back_populates='generated_reports')
    comments = relationship('ReportComment', back_populates='report', cascade='all, delete-orphan')
    

    @validates('report_name')
    def validate_report_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError("Report name must be at least 3 characters")
        return name.strip()

    @validates('file_format')
    def validate_file_format(self, key, fmt):
        if fmt.lower() not in ['json', 'csv', 'xml']:
            raise ValueError("Unsupported file format")
        return fmt.lower()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "report_name": self.report_name,
            "report_type": self.report_type,
            "file_format": self.file_format,
            "generated_by": self.generated_by,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "comment_count": len(self.comments),
            "generator_name": getattr(self.generator, 'name', None)
        }

    def __repr__(self) -> str:
        return f'<Report {self.id} "{self.report_name}" ({self.report_type})>'
