import logging

from flask import request, jsonify
from app.routes.patient import practitioner_bp
from server.app.models import User, CareTeam, FormTemplate
from app.database import db
from server.app.utils.helpers import get_current_user_object
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user
from flask_jwt_extended import get_jwt_identity


logger = logging.getLogger(__name__)


@practitioner_bp.route('/search-patients', methods=['GET'])
def search_patients(practitioner_username):
    try:
        current_practitioner_user = get_current_user_object()

        if not current_practitioner_user:
            logger.error(f"Internal error: current_practitioner_user is None for '{practitioner_username}'.")
            return jsonify(message="Unauthorized: User profile invalid or not found."), 401

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)

        if page < 1 or limit < 1:
            logger.warning(f"Invalid pagination parameters provided by '{current_practitioner_user.username}': page={page}, limit={limit}")
            return jsonify(message="Invalid pagination parameters. 'page' and 'limit' must be positive integers."), 400


        practitioner_id_for_query = current_practitioner_user.id

        query = CareTeam.query.filter_by(
            practitioner_id=practitioner_id_for_query,
            connected=True
        ).options(db.joinedload(CareTeam.patient))

        query = query.order_by(CareTeam.created_at.desc())

        patients_pagination = query.paginate(page=page, per_page=limit, error_out=False)

        patients_data = [care_team.to_dict() for care_team in patients_pagination.items]

        logger.info(f"Practitioner '{practitioner_username}' successfully retrieved {len(patients_data)} patients (Page {page}/{patients_pagination.pages}).")


        return jsonify({
            "patients": patients_data,
            "total_patients": patients_pagination.total, 
            "current_page": patients_pagination.page,
            "total_pages": patients_pagination.pages,
            "has_next": patients_pagination.has_next,
            "has_prev": patients_pagination.has_prev,
        }), 200 

    except Exception as e:
        logger.exception(f"An unexpected error occurred during practitioner search for patients '{practitioner_username}'.")
        return jsonify(message="An internal server error occurred while searching patients."), 500



@practitioner_bp.route('/search-form-templates', methods=['GET'])
def search_form_templates(practitioner_username):
    try:
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
    except Exception as e:
        logger.exception(f"An unexpected error occurred during practitioner search for form templates '{practitioner_username}'.")
        return jsonify(message="An internal server error occurred while searching patients."), 500
        







@practitioner_bp.route('/create-form-template', methods=['POST'])
def create_form_template(practitioner_username):
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

