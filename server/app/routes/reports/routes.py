from flask import request, jsonify
from app.routes.reports import reports_bp
from app.models.user import User
from app.database import db
from app.utils.auth_decorators import jwt_required_with_role,set_versioning_user
from flask_jwt_extended import get_jwt_identity

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from app.utils.auth_decorators import jwt_required_with_role


@reports_bp.route('/', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_medications():
    pass

@reports_bp.route('/<int:report_id>', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def view():
    pass

@reports_bp.route('/<int:report_id>/delete', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def delete():
    pass
