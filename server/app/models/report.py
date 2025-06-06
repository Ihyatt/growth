from typing import Dict, Any 

from sqlalchemy.orm import  validates
from sqlalchemy_continuum import make_versioned
from app.database import db

make_versioned(user_cls='app.models.user.User')

class Report(db.Model):
    __versioned__ = {}
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(255), nullable=False)
    report_data = db.Column(db.Text, nullable=False)
    file_format = db.Column(db.String(10), default='json')
    
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'))     
    practitioner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    is_deleted = db.Column(db.Boolean, default=False, nullable=False) 
    
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    report_reviewer = db.relationship('User', back_populates='reports_as_practitioner')
    reported_patient = db.relationship('User', back_populates='reports_as_patient')
    report_comments = db.relationship('ReportComment', back_populates='report')



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
            "report_data": self.report_data,
            "file_format": self.file_format,
            "patient_id": self.patient_id,
            "patient_username": self.patient_username, 
            "practitioner_id": self.practitioner_id,
            "is_deleted": self.is_deleted, 
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "comment_count": len(self.comments),
            "generator_username": getattr(self.generator, 'username', None),
            "patient_username_from_rel": getattr(self.patient_subject, 'username', None)
        }

    def __repr__(self) -> str:
        return f'<Report {self.id} "{self.report_name}">' 
    



make_versioned(user_cls='app.models.user.User')

class ReportComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    
    report_comment_author = db.relationship('User', back_populates='reports_comments', lazy=True)
    report = db.relationship('Report', back_populates='report_comments', lazy=True)



    def __repr__(self):
        return f'<MedicationComment {self.id} on Medication:{self.medication_id}>'

    def to_dict(self, include_user=True):
        data = {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "medication_id": self.medication_id,
            "user_id": self.user_id
        }
        
        return data
