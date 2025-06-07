from flask import request, jsonify
from app.routes.assigned_form import assigned_form_bp
from server.app.models.assigned_form import AssignedForm
from app.database import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.constants.enums import FormStatus, FormResponses
from server.app.utils.decorators import  set_versioning_user



@assigned_form_bp.route('/todo', methods=['POST'])
def get_user_forms():
    current_user_id = get_jwt_identity()
    forms = AssignedForm.query.filter_by(
        patient_user_id = current_user_id,
        status = FormStatus.TODO
    ).all()

    compiled_forms = []

    for form in forms:
    
        practitioner = form.assigned_form_bp.practitioner
    
        form_data = form.form_data
        status = form.status
        compiled_forms.append(
            {
                'practitioner': practitioner.username,
                'questions': form.form_template.questions,
                'answers': FormResponses,
                'form_data': form_data, 
                'status': status
            }
        )

    return jsonify({"compiled_forms": compiled_forms})