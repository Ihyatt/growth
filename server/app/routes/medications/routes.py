from flask import request, jsonify
from app.routes.medications import medications_bp
from app.models.user import User
from app.database import db
from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from app.utils.auth_decorators import jwt_required_with_role


@medications_bp.route('/', methods=['GET'])
def get_medications():
    pass

@medications_bp.route('/<int:medication_id>', methods=['GET'])
def view():
    pass


@medications_bp.route('/add', methods=['POST'])
def add():
    pass


@medications_bp.route('/<int:medication_id>/edit', methods=['POST'])
def edit():
    pass


@medications_bp.route('/delete', methods=['POST'])
def delete():
    pass