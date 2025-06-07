import logging
from flask import request, jsonify
from app.routes.report import report_bp
from server.app.models.form_template import Report, User, ReportComment
from app.database import db
from server.app.utils.helpers import audit_log_helper,get_current_user_object,resource_owner_or_admin_required, roles_required, care_giver_or_admin_required
from app.models.constants.enums import UserLevel, UserApprovalStatus, ProfileStatus, AuditActionStatus

from server.app.utils.decorators import set_versioning_user
from flask_jwt_extended import get_jwt_identity, jwt_required
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user, set_versioning_user



logger = logging.getLogger(__name__)


@report_bp.route('/', methods=['GET'])
@jwt_required()
@roles_required([UserLevel.ADMIN, UserLevel.PATIENT])
@resource_owner_or_admin_required(username_param_name='patient_username')
def get_report_as_patient(patient_username, report_id):
    try:
        current_patient_user = get_current_user_object()
        patient_user = User.query.filter_by(username=patient_username).first()

        if not patient_user or not current_patient_user:
            logger.error(f"Internal error: current_patient is None for '{patient_username}'.")
            return jsonify(message="Unauthorized: User profile invalid or not found."), 401

        if current_patient_user.id != patient_user.id:
            logger.error(f"Logged in user_id {current_patient_user.id } does not match the patient's user_id {patient_user.id}'.")
            return jsonify(message="Unauthorized: Logged in user does not match requested patient."), 403
        
        report =  Report.query.filter_by(report_id).first()
        
        if not report:
            logger.error(f"Requested report with report_id of {report_id } does not exist within Reports'.")
            return jsonify(message="Unauthorized: Report invalid or not found."), 404
        
        return jsonify({"report": report.to_dict()})
    
    except Exception as e:
        logger.exception(f"An unexpected error occurred during patient {patient_username} getting their report with id of {report_id}'.")
        return jsonify(message="An internal server error occurred while patient attempting to get their report."), 500


@report_bp.route('/delete', methods=['POST'])
@jwt_required()
@roles_required([UserLevel.ADMIN, UserLevel.PRACTITIONER])
@care_giver_or_admin_required(username_param_name='patient_username')
def delete_report_as_practitioner(patient_username, report_id):
    try:
        report_id = request.args.get('report_id')
        report = Report.query.filter_by(report_id).first()
        report_id.is_active = False
        db.session.commit()

    except Exception as e:
        logger.exception(f"Unable to delete report for report_id {report_id} for {patient_username} '.")
        return jsonify(message="An internal server error occurred while attempting to delete report."), 500

   

@report_bp.route('/create', methods=['POST'])
def create():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('text')

    new_comment = ReportComment(
        text=comment_text,
        user_id=current_user_id,
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201