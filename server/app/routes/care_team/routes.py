from flask import request, jsonify
from app.routes.care_team import care_team_bp
from app.models.user import User, CareTeam
from app.database import db
from server.app.utils.decorators import set_versioning_user

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from flask_jwt_extended import get_jwt_identity,jwt_required


# @set_versioning_user
# @jwt_required()

@care_team_bp.route('/start-care', methods=['POST'])
def start_care():

    patient_username = request.args.get('username')
    practitioner_username = request.args.get('username')
    patient_user = User.query.filter_by(username=patient_username).first()
    practitioner_user = User.query.filter_by(username=practitioner_username).first()
    start_care = CareTeam(patient_id=patient_user.id, practitioner_id=practitioner_user.id)

    db.session.commit()



# @set_versioning_user
# @jwt_required()
@care_team_bp.route('/end-care', methods=['POST'])
def end_care():

    patient_username = request.args.get('patient_username')
    practitioner_username = request.args.get('patient_username')
    patient_user = User.query.filter_by(username=patient_username).first()
    practitioner_user = User.query.filter_by(username=practitioner_username).first()

    end_care = CareTeam.query.filter_by(patient_id=patient_user.id, practitioner_id=practitioner_user.id).first()
    end_care.staus = False
    db.session.commit()