
from flask import request, jsonify
from app.routes.patients import patients_bp
from app.models.user import User, Medication,Follow
from app.database import db
from server.app.utils.decorators import enforce_role_practioner, enforce_role_patient, enforce_role_practioner, set_versioning_user
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.decorators import 

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from server.app.utils.decorators import jwt_required_with_role



@patients_bp.route('/search', methods=['GET'])
@enforce_role_practioner
def get_patients():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)

    query = Follow.query

    query = query.filter_by(practitioner_id=current_user_id, active=True)

    query = query.order_by(Follow.created_at.desc())
    
    patients_pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "forms": [patients.to_dict() for patients in patients_pagination.items],
        "total": patients_pagination.total,
        "page": patients_pagination.page,
        "pages": patients_pagination.pages,
        "has_next": patients_pagination.has_next,
        "has_prev": patients_pagination.has_prev,
    })



@patients_bp.route('/<str:username>', methods=['GET'])
@enforce_role_practioner
def get_patient():
    current_user_id = get_jwt_identity()
    patient_username = request.args.get('username')

    patient_user =  User.query.get(username=patient_username)
    follow = Follow.query.get(
        practitioner_id=current_user_id,
        patient_id=patient_user.id
    )
    follow.is_active = False
    db.session.commit()

    return jsonify({"medication": 'unfollowed'})
    

    practitioner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    active = Column(Boolean, default=True, nullable=False)