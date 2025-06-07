from flask import Blueprint
from app.routes.reports.comments.routes import report_comment_bp


report_bp = Blueprint('reports', __name__, url_prefix='/reports')
report_bp.register_blueprint(report_comment_bp)