
from flask import request, jsonify
from app.routes.admin.routes import admin_bp
from app.models.user import User
from app.database import db
from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from server.app.utils.decorators import enforce_role_admin, set_versioning_user, enforce_role_patient
from app.utils.audit_log import log_audit


@admin_bp.route('/users', methods=['GET'])
@set_versioning_user
@enforce_role_admin
def get_admin_users():
    try:
        validation_map = {
            'pending': ValidationLevel.PENDING,
            'approved': ValidationLevel.APPROVED 
        }
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        status_param = request.args.get('status')
        active_param = request.args.get('active')
        email_param = request.args.get('email')
        active = True if active_param == 'ACTIVE' else False
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
            "has_prev": users_pagination.has_prev
        })

    except Exception as e:
        db.session.rollback()
        return jsonify(error="Query failed: " + str(e)), 500


@admin_bp.route('/approve', methods=['POST'])
@set_versioning_user
@enforce_role_admin
def approve_user():
    try:
        data = request.get_json()
        user_id = data.get('userId')

        if not user_id:
            return jsonify({"message": "User ID is required."}), 400

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"message": "User not found."}), 404


        if user.is_validated == ValidationLevel.APPROVED:
            return jsonify({"message": f"User {user.email} is already approved."}),
        
        old_validation_level = user.is_validated

        user.is_validated = ValidationLevel.APPROVED

        audit_details = {
            'old_validation_level': old_validation_level,
            'new_validation_level': user.is_validated
        }
        log_audit(
            target_user_id=user.id,
            action_type=AuditActionType.APPROVED,
            details=audit_details
        )
        db.session.commit()

        return jsonify({
            "message": f"User {user.email} approved successfully.",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to approve user: {str(e)}"}), 

