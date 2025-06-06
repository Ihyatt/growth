from flask import Blueprint
from app.routes.medications.comments.routes import medications_comments_bp


medications_bp = Blueprint('medications', __name__, url_prefix='/medications')
medications_bp.register_blueprint(medications_comments_bp)

