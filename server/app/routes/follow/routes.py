from flask import request, jsonify
from app.routes.medications.comments import medications_comments_bp
from app.models.user import User
from app.database import db
from server.app.utils.decorators import set_versioning_user

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from flask_jwt_extended import get_jwt_identity,jwt_required


@medications_comments_bp.route('/', methods=['GET'])
@set_versioning_user
@jwt_required()
def follow():
    pass

@medications_comments_bp.route('/add', methods=['POST'])
@set_versioning_user
@jwt_required()
def unfollow():
    pass


