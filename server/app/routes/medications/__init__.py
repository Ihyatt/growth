from flask import Blueprint
from app.routes.comments.routes import comments_bp


medications_bp = Blueprint('medications', __name__, url_prefix='/medications')
medications_bp.register_blueprint(comments_bp)


