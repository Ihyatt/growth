from flask import Blueprint
from app.routes.reports.routes import reports_bp
from app.routes.patients_forms.routes import patients_forms_bp
from app.routes.medications.routes import medications_bp


reports_bp = Blueprint('patients', __name__, url_prefix='/patients')
reports_bp.register_blueprint(reports_bp)
reports_bp.register_blueprint(patients_forms_bp)
reports_bp.register_blueprint(medications_bp)

