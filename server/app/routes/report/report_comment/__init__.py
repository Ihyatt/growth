from flask import Blueprint


report_comment_bp = Blueprint('report_comment', __name__, url_prefix='/report_comments/<int:report_comment_id>')