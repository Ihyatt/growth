from flask import request, jsonify
from app.routes.patient import therapist_bp
from app.models.user import User, CareTeam, FormTemplate
from app.database import db
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user
from flask_jwt_extended import get_jwt_identity


@therapist_bp.route('/search', methods=['GET'])
def search():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)

    query = CareTeam.query

    query = query.filter_by(practitioner_id=current_user_id, active=True)

    query = query.order_by(CareTeam.created_at.desc())
    
    patients_pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "forms": [patients.to_dict() for patients in patients_pagination.items],
        "total": patients_pagination.total,
        "page": patients_pagination.page,
        "pages": patients_pagination.pages,
        "has_next": patients_pagination.has_next,
        "has_prev": patients_pagination.has_prev,
    })


@therapist_bp.route('/search-form-template', methods=['GET'])
def get_form_template():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    title = request.args.get('title')
    status = request.args.get('status')
    query = FormTemplate.query

    #verify curr user if is equal toe practitioner id

    query = query.filter_by(practitioner_id=current_user_id, status=status)

    if title:
        query = query.filter(FormTemplate.title.ilike(f'%{title}%'))

    query = query.order_by(FormTemplate.created_at.desc())
    
    forms_pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "forms": [form.to_dict() for form in forms_pagination.items],
        "total": forms_pagination.total,
        "page": forms_pagination.page,
        "pages": forms_pagination.pages,
        "has_next": forms_pagination.has_next,
        "has_prev": forms_pagination.has_prev,
    })




@therapist_bp.route('/create', methods=['POST'])
def create():
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    title = data.get('title')
    questions = data.get('questions')

    practitioner_form = FormTemplate(
        title=title,
        questions=questions,
        practitoner_id=current_user_id
    )

    db.session.add(practitioner_form)
    db.session.commit()

    return jsonify(message="file created") 

