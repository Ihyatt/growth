from flask import request, jsonify
from app.routes.assigned_form import assigned_form_bp
from server.app.models.assigned_form import AssignedForm, User
from app.models.constants.enums import UserLevel, UserApprovalStatus, ProfileStatus, AuditActionStatus

from app.database import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.constants.enums import FormStatus, FormResponses
from server.app.utils.decorators import  set_versioning_user



@assigned_form_bp.route('/patient', methods=['GET'])
def get_assigned_forms_as_patient(patient_username, assigned_form_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(username=patient_username).first()

        if not user:
            return jsonify({"message": "User not found."}), 404
        
        if user.id != current_user_id:
            return jsonify({"message": "You are not the correct user"}), 404
        
        if user.user_level != UserLevel.PATIENT:
            return jsonify({"message": "You are not a patient"}), 404

        assigned_form = AssignedForm.query.filter_by(
            patient_user_id = current_user_id,
            id=assigned_form_id,
            status = FormStatus.TODO
        ).first()

        return jsonify({"assigned_form": assigned_form, "form_reponses": FormResponses}), 200
    
    except Exception as e:
        print(f"Error fetching assigned form for practitioner: {e}")
        return jsonify(error="Failed to fetch assigned form: " + str(e)), 500
    


@assigned_form_bp.route('/patient', methods=['POST'])
def submit_assigned_form_as_patient(patient_username, assigned_form_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(username=patient_username).first()

        if not user:
            return jsonify({"message": "User not found."}), 404
        
        if user.id != current_user_id:
            return jsonify({"message": "You are not the correct user"}), 404
        
        if user.user_level != UserLevel.PATIENT:
            return jsonify({"message": "You are not a patient"}), 404

        assigned_form = AssignedForm.query.filter_by(
            patient_user_id = current_user_id,
            id=assigned_form_id,
            status = FormStatus.TODO
        ).first()


        if not assigned_form:
            return jsonify({"message": "Assigned form not found for this patient/ID or practitioner."}), 404

        assigned_form.status = FormStatus.COMPLETED
        assigned_form.form_data = 

        return jsonify({"assigned_form": assigned_form, "form_reponses": FormResponses}), 200
    
    
    except Exception as e:
        print(f"Error fetching assigned form for practitioner: {e}")
        return jsonify(error="Failed to fetch assigned form: " + str(e)), 500

@assigned_form_bp.route('/practitioner', methods=['GET'])
def get_assigned_forms_as_practitioner(practitioner_username, patient_username, assigned_form_id):
    try:
        current_user_id = get_jwt_identity()
        patient_user = User.query.filter_by(username=patient_username).first()
        practitioner_user = User.query.filter_by(username=practitioner_username).first()

        if not patient_user or not practitioner_user:
            return jsonify({"message": "Target patient or practitioner username invalid."}), 404
        
        if practitioner_user.id != current_user_id:
            return jsonify({"message": "You are not the correct user"}), 403
        
        if practitioner_user.user_level != UserLevel.PRACTITIONER:
            return jsonify({"message": "You are not a practitioner"}), 403

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