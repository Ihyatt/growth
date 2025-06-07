from flask import Blueprint

from app.routes.report.routes import report_bp
from app.routes.care_team.routes import care_team_bp
from app.routes.form_template.routes import form_template_bp
from app.routes.medication.routes import medication_bp
from app.routes.assigned_form.routes import assigned_form_bp
from app.routes.patient.routes import patient_bp
from app.routes.practitioner.routes import practitioner_bp


admin_bp = Blueprint('admin', __name__, url_prefix='/admins/<int:user_id>')
admin_bp.register_blueprint(care_team_bp)
admin_bp.register_blueprint(form_template_bp)
admin_bp.register_blueprint(report_bp)
admin_bp.register_blueprint(medication_bp)
admin_bp.register_blueprint(assigned_form_bp)
admin_bp.register_blueprint(patient_bp)
admin_bp.register_blueprint(practitioner_bp)
