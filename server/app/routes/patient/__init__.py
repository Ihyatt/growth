from flask import Blueprint
from app.routes.report.routes import report_bp
from app.routes.assigned_form.routes import assign_form_bp
from app.routes.medication.routes import medication_bp


patient_bp = Blueprint('patients', __name__, url_prefix='/patients/<str:patient_username>')
patient_bp.register_blueprint(report_bp)
patient_bp.register_blueprint(assign_form_bp)
patient_bp.register_blueprint(medication_bp)