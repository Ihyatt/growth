from flask import Blueprint
from app.routes.patient.routes import patient_bp
from app.routes.form_template.routes import form_template_bp


therapist_bp = Blueprint('therapist', __name__, url_prefix='/therapists/<str:therapist_username>')
therapist_bp.register_blueprint(patient_bp)
therapist_bp.register_blueprint(form_template_bp)
