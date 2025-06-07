from flask import Blueprint
from app.routes.patient.routes import patient_bp
from app.routes.form_template.routes import form_template_bp


practitioner_bp = Blueprint('practitioners', __name__, url_prefix='/practitioners/<str:practitioner_username>')
practitioner_bp.register_blueprint(patient_bp)
practitioner_bp.register_blueprint(form_template_bp)
