from flask import request, jsonify
from app.routes.forms import forms_bp
from server.app.models.patient_form import UserForm, User, PractitionerForm
from app.database import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.constants.enums import FormStatus, FormResponses
from server.app.utils.decorators import  set_versioning_user


"""
PATIENT APIS
"""   
     
@forms_bp.route('/todo', methods=['POST'])
@set_versioning_user
@jwt_required()
def get_user_forms():
    current_user_id = get_jwt_identity()
    forms = UserForm.query.filter_by(
        patient_user_id = current_user_id,
        status = FormStatus.TODO
    ).all()

    compiled_forms = []

    for form in forms:
    
        practitioner = form.practitioner_form.practitioner
    
        form_data = form.form_data
        status = form.status
        compiled_forms.append(
            {
                'practitioner': practitioner.username,
                'questions': form.practitioner_form.questions,
                'answers': FormResponses,
                'form_data': form_data, 
                'status': status
            }
        )

    return jsonify({"compiled_forms": compiled_forms})
 