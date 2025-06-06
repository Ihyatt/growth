from flask import request, jsonify
from app.routes.medications import medications_bp
from app.models.user import User
from app.database import db
from server.app.utils.decorators import jwt_required_with_role,set_versioning_user
from flask_jwt_extended import get_jwt_identity

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from server.app.utils.decorators import jwt_required_with_role


@medications_bp.route('/', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_medications():
    pass

@medications_bp.route('/<int:medication_id>', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def view():
    pass


@medications_bp.route('/add', methods=['POST'])
@set_versioning_user
@jwt_required_with_role
def add():
    pass


@medications_bp.route('/<int:medication_id>/edit', methods=['POST'])
@set_versioning_user
@jwt_required_with_role
def edit():
    pass


@medications_bp.route('/delete', methods=['POST'])
@set_versioning_user
@jwt_required_with_role
def delete():
    pass