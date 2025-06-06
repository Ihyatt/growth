from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from sqlalchemy import Enum 
from app.models.constants.enums import PermissionLevel, ValidationLevel
from sqlalchemy_continuum import make_versioned



make_versioned(user_cls=None)

class Report(db.Model):
    __versioned__ = {}
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    report_name = db.Column(db.String(255), nullable=False)
    report_type = db.Column(db.String(100), nullable=False)  # e.g., "weekly_summary"
    report_data = db.Column(db.Text, nullable=False)  # This stores the actual CSV or JSON string
    generated_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # optional
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "report_name": self.report_name,
            "report_type": self.report_type,
            "report_data": self.report_data
        }
    

make_versioned(user_cls=None)

class ReportComment(db.Model):
    __versioned__ = {}
    __tablename__ = 'report_comments'
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))    
    updated_at = db.Column(db.DateTime, 
                         default=datetime.now(timezone.utc),
                         onupdate=datetime.now(timezone.utc))
