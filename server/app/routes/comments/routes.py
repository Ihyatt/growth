
from flask import request, jsonify
from app.routes.forms import forms_bp
from app.models.user_form import UserForm, User, PractitionerForm
from app.database import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.constants.enums import FormStatus, FormResponses
from server.app.utils.decorators import enforce_role_practioner, enforce_role_patient, enforce_role_practioner, set_versioning_user
from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType #this needs to be set up for permissions, or actually i can use a decoratore


@forms_bp.route('/create', methods=['GET'])
@jwt_required()
def create():
    current_user_id = get_jwt_identity()


    return jsonify()


@forms_bp.route('/edit/<int:form_id>', methods=['GET'])
@jwt_required()
def edit():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    status = request.args.get('status')
    owner = request.args.get('owner')

    user = User.query.get(username = owner)

    query = UserForm.query

    query = query.filter_by(
        patient_user_id = user.user_id,
        status = status
    ).all()

    forms_pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "forms": [form.to_dict() for form in forms_pagination.items],
        "total": forms_pagination.total,
        "page": forms_pagination.page,
        "pages": forms_pagination.pages,
        "has_next": forms_pagination.has_next,
        "has_prev": forms_pagination.has_prev,
    })

 
@forms_bp.route('delete/<int:form_id>', methods=['GET'])
@jwt_required()
def delete(form_id):
    
    current_user_id = get_jwt_identity() 
    form_id = request.args.get('form_id')
    form = PractitionerForm.query.get(practitioner_id=current_user_id, id=form_id)

    return jsonify({'form':form})
     
  