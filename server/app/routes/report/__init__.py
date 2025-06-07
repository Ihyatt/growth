from flask import Blueprint
from app.routes.report.report_comment.routes import report_comment_bp


report_bp = Blueprint('reports', __name__, url_prefix='/reports/<int:report_id>')
report_bp.register_blueprint(report_comment_bp)