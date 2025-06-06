
from flask import request, jsonify
from app.routes.forms import forms_bp
from app.models.user_form import UserForm, User, PractitionerForm
from app.database import db
from flask_jwt_extended import get_jwt_identity
from app.models.constants.enums import FormStatus, FormResponses



from app.utils.auth_decorators import jwt_required_with_role,set_versioning_user

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType


@forms_bp.route('/search/my_forms', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_practitoner_forms():

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        title = request.args.get('title')
        status = request.args.get('status')
        query = PractitionerForm.query

        query = query.filter_by(status=status)
        if title:
            query = query.filter(PractitionerForm.title.ilike(f'%{title}%'))
        
        forms_pagination = query.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            "forms": [form.to_dict() for form in forms_pagination.items],
            "total": forms_pagination.total,
            "page": forms_pagination.page,
            "pages": forms_pagination.pages,
            "has_next": forms_pagination.has_next,
            "has_prev": forms_pagination.has_prev,
        })


@forms_bp.route('/search/patients_forms', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_patients_forms():

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        title = request.args.get('title')
        status = request.args.get('status')
        owner = request.args.get('owner')
        query = User.query

        query = query.filter_by(
            permission=PermissionLevel.PRACTITIONER,
            is_validated=validation_map[status_param],
            is_active=active,
        )
        if email_param:
            query = query.filter(User.email.ilike(f'%{email_param}%'))
        users_pagination = query.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            "users": [user.to_dict() for user in users_pagination.items],
            "total": users_pagination.total,
            "page": users_pagination.page,
            "pages": users_pagination.pages,
            "has_next": users_pagination.has_next,
            "has_prev": users_pagination.has_pre
 
@forms_bp.route('/my_forms/<int:form_id>', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_practitoner_form():

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        title = request.args.get('title')
        status = request.args.get('status')
        owner = request.args.get('owner')
        query = User.query

        query = query.filter_by(
            permission=PermissionLevel.PRACTITIONER,
            is_validated=validation_map[status_param],
            is_active=active,
        )
        if email_param:
            query = query.filter(User.email.ilike(f'%{email_param}%'))
        users_pagination = query.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            "users": [user.to_dict() for user in users_pagination.items],
            "total": users_pagination.total,
            "page": users_pagination.page,
            "pages": users_pagination.pages,
            "has_next": users_pagination.has_next,
            "has_prev": users_pagination.has_pre

@forms_bp.route('/patients/<int:form_id>', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_patient_form():

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        title = request.args.get('title')
        status = request.args.get('status')
        owner = request.args.get('owner')
        query = User.query

        query = query.filter_by(
            permission=PermissionLevel.PRACTITIONER,
            is_validated=validation_map[status_param],
            is_active=active,
        )
        if email_param:
            query = query.filter(User.email.ilike(f'%{email_param}%'))
        users_pagination = query.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            "users": [user.to_dict() for user in users_pagination.items],
            "total": users_pagination.total,
            "page": users_pagination.page,
            "pages": users_pagination.pages,
            "has_next": users_pagination.has_next,
            "has_prev": users_pagination.has_pre



@forms_bp.route('/todo', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def get_user_forms():
    
    current_user_id = get_jwt_identity()
    forms = UserForm.query.filter_by(
        patient_user_id = current_user_id,
        status = FormStatus.TODO
    ).all()

    compiled_forms = []

    for form in forms:
        practitioner_form = db.session.get(PractitionerForm, form.practitioner_form_id)
        practitioner = db.session.get(User, practitioner_form.practitioner_id)

        practitioner_username = practitioner.username
        form_data = form.form_data
        status = form.status
        compiled_forms.append(
            {
                'practitioner': practitioner_username,
                'questions': practitioner_form.questions,
                'answers': FormResponses,
                'form_data': form_data, 
                'status': status
            }
        )

    return jsonify({"compiled_forms": compiled_forms})
 

@forms_bp.route('/create', methods=['GET'])
@set_versioning_user
@jwt_required_with_role
def create():
    pass


@forms_bp.route('/archive', methods=['GET'])
def archive():
    pass