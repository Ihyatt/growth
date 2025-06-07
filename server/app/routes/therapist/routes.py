from flask import request, jsonify
from app.routes.patient import therapist_bp
from app.models.user import User, CareTeam
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
