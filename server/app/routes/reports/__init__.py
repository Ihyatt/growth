from flask import Blueprint
from app.routes.comments.routes import comments_bp


reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
reports_bp.register_blueprint(comments_bp)

