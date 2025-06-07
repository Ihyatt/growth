from flask import request, jsonify
from app.routes.patient import therapist_bp, patient_bp
from app.models.user import User, AssignForm
from app.database import db
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user
from flask_jwt_extended import get_jwt_identity


@patient_bp.route('/scroll', methods=['GET']) #this is only for patients
def scroll_forms():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)


    query = AssignForm.query.filter_by(patient_id=current_user_id, active=True)

    query = query.order_by(AssignForm.created_at.desc())
    
    forms_pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "forms": [form.to_dict() for form in forms_pagination.items],
        "total": forms_pagination.total,
        "page": forms_pagination.page,
        "pages": forms_pagination.pages,
        "has_next": forms_pagination.has_next,
        "has_prev": forms_pagination.has_prev,
    })



@patient_bp.route('/medications', methods=['GET'])
def get_medications(therapist_username, patient_username):
    patient_username = request.args.get('username')
    patient_user =  User.query.filter_by(username=patient_username).first()
    medications = patient_user.medications


    return jsonify({
        "medications": [medication.to_dict() for medication in medications.items]
    })

