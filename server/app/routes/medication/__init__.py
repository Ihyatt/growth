from flask import Blueprint
from app.routes.medications.comments.routes import medication_comment_bp


medication_bp = Blueprint('medications', __name__, url_prefix='/medications')
medication_bp.register_blueprint(medication_comment_bp)