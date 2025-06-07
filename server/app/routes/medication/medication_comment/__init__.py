from flask import Blueprint


medication_comment_bp = Blueprint('medication_comment', __name__, url_prefix='/medication_comments/<int:medication_comment_id>')