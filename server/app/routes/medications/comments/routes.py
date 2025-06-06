from flask import request, jsonify
from app.routes.medications.comments import medications_comments_bp
from app.models.user import User
from app.database import db
from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from app.utils.auth_decorators import jwt_required_with_role


@medications_comments_bp.route('/', methods=['GET'])
def get_comments():
    pass

@medications_comments_bp.route('/add', methods=['POST'])
def add():
    pass


@medications_comments_bp.route('<int:comment_id>/edit', methods=['POST'])
def edit():
    pass


@medications_comments_bp.route('<int:comment_id>/delete', methods=['POST'])
def delete():
    pass