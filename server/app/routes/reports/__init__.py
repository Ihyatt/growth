from flask import Blueprint
from app.routes.reports.comments.routes import report_comments_bp


reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
reports_bp.register_blueprint(report_comments_bp)

