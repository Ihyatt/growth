from flask import request, jsonify
from app.routes.follow import follow_bp
from app.models.user import User,Follow
from app.database import db
from server.app.utils.decorators import set_versioning_user

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from flask_jwt_extended import get_jwt_identity,jwt_required


@follow_bp.route('/follow/<str:username>', methods=['POST'])
@set_versioning_user
@jwt_required()
def follow():

    patient_username = request.args.get('username')
    practitioner_username = request.args.get('username')
    patient_user = User.query.get(username=patient_username)
    practitioner_user = User.query.get(username=practitioner_username)
    new_follow = Follow(patient_id=patient_user.id, practitioner_id=practitioner_user.id)

    db.session.commit()


@follow_bp.route('/unfollow/<str:username>', methods=['POST'])
@set_versioning_user
@jwt_required()
def unfollow():

    patient_username = request.args.get('patient_username')
    practitioner_username = request.args.get('patient_username')
    patient_user = User.query.get(username=patient_username)
    practitioner_user = User.query.get(username=practitioner_username)

    un_follow = Follow.query.get(patient_id=patient_user.id, practitioner_id=practitioner_user.id)
    un_follow.staus = False
    db.session.commit()

