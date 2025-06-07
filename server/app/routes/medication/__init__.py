from flask import Blueprint
from app.routes.medication.medication_comment.routes import medication_comment_bp


medication_bp = Blueprint('medications', __name__, url_prefix='/medications/<int:medication_id>')
medication_bp.register_blueprint(medication_comment_bp)