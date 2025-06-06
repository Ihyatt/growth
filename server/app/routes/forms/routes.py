
from flask import request, jsonify
from app.routes.forms import forms_bp
from app.models.user import User
from app.database import db
from app.utils.auth_decorators import jwt_required_with_role,set_versioning_user

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from app.utils.auth_decorators import jwt_required_with_role


@forms_bp.route('/', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_forms():
    pass

@forms_bp.route('/<int:form_id>', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def view():
    pass

@forms_bp.route('/create', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def create():
    pass


@forms_bp.route('/archive', methods=['GET'])
def archive():
    pass