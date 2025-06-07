from flask import Blueprint
from app.routes.report.routes import report_bp
from app.routes.patients_forms.routes import patients_form_bp
from app.routes.medication.routes import medication_bp


report_bp = Blueprint('patients', __name__, url_prefix='/patients')
report_bp.register_blueprint(report_bp)
report_bp.register_blueprint(patients_form_bp)
report_bp.register_blueprint(medication_bp)