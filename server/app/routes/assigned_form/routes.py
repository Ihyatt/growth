from flask import request, jsonify
from app.routes.assigned_form import assigned_form_bp
from server.app.models.assigned_form import AssignedForm, User
from app.models.constants.enums import UserLevel, UserApprovalStatus, ProfileStatus, AuditActionStatus
from server.app.utils.helpers import audit_log_helper,get_current_user_object,resource_owner_or_admin_required, roles_required, care_giver_or_admin_required
from app.database import db
from sqlalchemy.exc import StaleDataError # Crucial for handling conflicts

from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.constants.enums import FormStatus, FormResponses
from server.app.utils.decorators import  set_versioning_user
    



@assigned_form_bp.route('/todo', methods=['GET'])
@jwt_required()
@resource_owner_or_admin_required(username_param_name='patient_username')
@roles_required([UserLevel.ADMIN, UserLevel.PATIENT])
def get_assigned_forms_as_patient(practitioner_username, patient_username, assigned_form_id):
    try:
        patient_user = User.query.filter_by(username=patient_username).first()
        practitioner_user = User.query.filter_by(username=practitioner_username).first()

        assigned_form = AssignedForm.query.filter_by(
            patient_user_id = patient_user.id,
            id=assigned_form_id,
            reviewed_by_id = practitioner_user.id
            status = FormStatus.COMPLETED
        ).first()

        if not assigned_form:
            return jsonify({"message": "Assigned form not found for this patient/ID or practitioner."}), 404

        return jsonify({"assigned_form": assigned_form, "form_reponses": FormResponses}), 200
    
    except Exception as e:
        print(f"Error fetching assigned form for practitioner: {e}")
        return jsonify(error="Failed to fetch assigned form: " + str(e)), 500





@assigned_form_bp.route('/submit', methods=['POST'])
@jwt_required()
@resource_owner_or_admin_required(username_param_name='patient_username')
@roles_required([UserLevel.ADMIN, UserLevel.PATIENT])
def submit_assigned_form_as_patient(patient_username, assigned_form_id):
    try:
        user = User.query.filter_by(username=patient_username).first()
        request_data = request.get_json()
        form_data = request_data.get('form_data')


        assigned_form = AssignedForm.query.filter_by(
            patient_user_id = current_user_id,
            id=assigned_form_id,
            status = FormStatus.TODO,
        ).first()


        if not assigned_form:
            return jsonify({"message": "Assigned form not found for this patient/ID or practitioner."}), 404

        assigned_form.status = FormStatus.COMPLETED
        assigned_form.form_data = form_data
        try:
            assigned_form.commit() 
        
        except StaleDataError as e:

            assigned_form.rollback()
     

        return jsonify({"assigned_form": assigned_form, "form_reponses": FormResponses}), 200
    
    
    except Exception as e:
        print(f"Error fetching assigned form for practitioner: {e}")
        return jsonify(error="Failed to fetch assigned form: " + str(e)), 500



@assigned_form_bp.route('/completed', methods=['GET'])
@jwt_required()
@care_giver_or_admin_required
@roles_required([UserLevel.ADMIN, UserLevel.PRACTITIONER])
def get_assigned_forms_as_practitioner(practitioner_username, patient_username, assigned_form_id):
    try:
        patient_user = User.query.filter_by(username=patient_username).first()
        practitioner_user = User.query.filter_by(username=practitioner_username).first()


        assigned_form = AssignedForm.query.filter_by(
            patient_user_id = patient_user.id,
            id=assigned_form_id,
            reviewed_by_id = practitioner_user.id
            status = FormStatus.COMPLETED
        ).first()

        if not assigned_form:
            return jsonify({"message": "Assigned form not found for this patient/ID or practitioner."}), 404

        return jsonify({"assigned_form": assigned_form, "form_reponses": FormResponses}), 200
    
    except Exception as e:
        print(f"Error fetching assigned form for practitioner: {e}")
        return jsonify(error="Failed to fetch assigned form: " + str(e)), 500