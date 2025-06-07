
from flask import request, jsonify
from app.routes.forms import forms_bp
from server.app.models.patient_form import UserForm, User, PractitionerForm
from app.database import db
from flask_jwt_extended import get_jwt_identity
from app.models.constants.enums import FormStatus
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user, set_versioning_user


@forms_bp.route('/search', methods=['GET'])
@enforce_elite_user
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


@forms_bp.route('/patients-forms', methods=['GET'])
@enforce_elite_user
def get_patients_forms():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    status = request.args.get('status')
    owner = request.args.get('owner')

    user = User.query.filter_by(username = owner).first()

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

 
@forms_bp.route('/<int:form_id>', methods=['GET'])
@enforce_elite_user
def get_practitoner_form(form_id):
    
    current_user_id = get_jwt_identity() 
    form_id = request.args.get('form_id')
    form = PractitionerForm.query.filter_by(practitioner_id=current_user_id, id=form_id).first()

    return jsonify({'form':form})
     
     
    
@forms_bp.route('/patient-form/<int:form_id>', methods=['GET'])
@enforce_elite_user
def get_patient_form():
    form_id = request.args.get('form_id')
    form = UserForm.query.filter_by(id=form_id).first()

    return jsonify({'form':form})



@forms_bp.route('/create', methods=['POST'])
@set_versioning_user
@enforce_elite_user
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
@enforce_elite_user
def archive_form():
    form_id = request.args.get('form_id')
    form = PractitionerForm.query.filter_by(id=form_id).first()
    form.status = FormStatus.ARCHIVED
    db.session.commit()


