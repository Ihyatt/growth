from flask import request, jsonify
from app.routes.reports import reports_comments_bp
from app.models.user import User
from app.database import db
from server.app.utils.decorators import jwt_required_with_role,set_versioning_user

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from server.app.utils.decorators import jwt_required_with_role


@reports_comments_bp.route('/', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_comments():
    pass

@reports_comments_bp.route('/add', methods=['POST'])
@set_versioning_user
@jwt_required_with_role
def add():
    pass


@reports_comments_bp.route('<int:comment_id>/edit', methods=['POST'])
@set_versioning_user
@jwt_required_with_role
def edit():
    pass


@reports_comments_bp.route('<int:comment_id>/delete', methods=['POST'])
@set_versioning_user
@jwt_required_with_role
def delete():
    pass