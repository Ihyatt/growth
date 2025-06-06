
from flask import request, jsonify
from app.routes.forms import forms_bp
from app.models.user_form import UserForm, User, PractitionerForm
from app.database import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.constants.enums import FormStatus, FormResponses
from server.app.utils.decorators import enforce_role_practioner, enforce_role_patient, enforce_role_practioner, set_versioning_user
from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType #this needs to be set up for permissions, or actually i can use a decoratore




"""
PRACTITIONER APIS
"""


@forms_bp.route('/search/my_forms', methods=['GET'])
@enforce_role_practioner
def get_practitoner_forms():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    title = request.args.get('title')
    status = request.args.get('status')
    query = PractitionerForm.query

    query = query.filter_by(practitioner_id=current_user_id, status=status)

    if title:
        query = query.filter(PractitionerForm.title.ilike(f'%{title}%'))

    query = query.order_by(PractitionerForm.created_at.desc())
    
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
@jenforce_role_practioner
def get_patients_forms():
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

 
@forms_bp.route('/my_forms/<int:form_id>', methods=['GET'])
@enforce_role_practioner
def get_practitoner_form(form_id):
    
    current_user_id = get_jwt_identity() 
    form_id = request.args.get('form_id')
    form = PractitionerForm.query.get(practitioner_id=current_user_id, id=form_id)

    return jsonify({'form':form})
     
     
    
@forms_bp.route('/patients/<int:form_id>', methods=['GET'])
@enforce_role_practioner
def get_patient_form():
    current_user_id = get_jwt_identity() #use this for permission validation
    form_id = request.args.get('form_id')
    form = UserForm.query.get(id=form_id)

    return jsonify({'form':form})



@forms_bp.route('/create', methods=['POST'])
@set_versioning_user
@enforce_role_practioner
def create():
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    title = data.get('title')
    questions = data.get('questions')

    practitioner_form = PractitionerForm(
        title=title,
        questions=questions,
        practitoner_id=current_user_id
    )

    db.session.add(practitioner_form)
    db.session.commit()

    return jsonify(message="file created") 



@forms_bp.route('/archive/<int:form_id>', methods=['POST'])
@enforce_role_practioner
def archive():
    current_user_id = get_jwt_identity()
    form_id = request.args.get('form_id')
    form = PractitionerForm.query.get(id=form_id)
    form.status = FormStatus.ARCHIVED



"""
PATIENT APIS
"""

    
     
     
@forms_bp.route('/todo', methods=['POST'])
@set_versioning_user
@enforce_role_patient
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
 