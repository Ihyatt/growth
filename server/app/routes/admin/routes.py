
from flask import request, jsonify
from app.routes.admin.routes import admin_bp
from app.models.user import User
from app.database import db
from app.models.constants.enums import UserLevel,ApprovalStatus,ProfileStatus,AuditActionStatus
from server.app.utils.decorators import enforce_role_admin, set_versioning_user
from app.utils.audit_log import log_audit
from flask_jwt_extended import get_jwt_identity


@admin_bp.route('/search', methods=['GET'])
@set_versioning_user
@enforce_role_admin
def get_users():
    try:
        approval_status_map = {
            'PENDING': ApprovalStatus.PENDING,
            'APPROVED': ApprovalStatus.APPROVED,
            'REJECTED': ApprovalStatus.REJECTED, 
        }
        user_level_status_map = {
            'PATIENT': UserLevel.PATIENT,
            'PRACTITIONER': UserLevel.PRACTITIONER,
            'ADMIN': UserLevel.ADMIN, 
        }
        profile_status_map = {
            'ACTIVE': ProfileStatus.ACTIVE,
            'INACTIVE': ProfileStatus.INACTIVE,
            'ADMIN': UserLevel.ADMIN, 
        }

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        status_param = request.args.get('status')
        profile_status_param = request.args.get('active')
        email_param = request.args.get('email')
        username_param = request.args.get('username')
        user_level_param = request.args.get('user_level')
        query = User.query

        query = query.filter_by(
            approval_status=approval_status_map[status_param],
            user_level=user_level_status_map[user_level_param],
            profile_status=profile_status_map[profile_status_param],
        )
        
        if email_param:
            query = query.filter(User.email.ilike(f'%{email_param}%'))
        
        if username_param:
            query = query.filter(User.username.ilike(f'%{username_param}%'))

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
def approve_practioners():
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        user_id = data.get('userId')

        if not user_id:
            return jsonify({"message": "User ID is required."}), 400

        user = User.query.filter_by(id=user_id).first()

        if user.user_level != UserLevel.PRACTITIONER:
            return jsonify({'message': 'user is not a practioner'}), 404

        if not user:
            return jsonify({"message": "User not found."}), 404

        if user.is_validated == UserLevel.APPROVED:
            return jsonify({"message": f"User {user.email} is already approved."}),
        
        old_validation_level = user.is_validated

        user.is_validated = UserLevel.APPROVED

        audit_details = {
            'old_validation_level': old_validation_level,
            'new_validation_level': user.is_validated
        }
        log_audit(
            admin_id=admin_id
            audited_id=user.id,
            action_type=AuditActionStatus.APPROVED,
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


@admin_bp.route('/reject', methods=['POST'])
@set_versioning_user
@enforce_role_admin
def reject_practioners():
    try:
        data = request.get_json()
        user_id = data.get('userId')

        if not user_id:
            return jsonify({"message": "User ID is required."}), 400

        user = User.query.filter_by(id=user_id).first()

        if user.user_level != UserLevel.PRACTITIONER:
            return jsonify({'message': 'user is not a practioner'}), 404

        if not user:
            return jsonify({"message": "User not found."}), 404


        if user.approval_status == ApprovalStatus.REJECTED:
            return jsonify({"message": f"User {user.email} is already rejected."}),
        
        old_validation_level = user.is_validated

        user.approval_status = ApprovalStatus.REJECTED

        audit_details = {
            'old_validation_level': old_validation_level,
            'new_validation_level': user.is_validated
        }
        log_audit(
            target_user_id=user.id,
            action_type=AuditActionStatus.SET_TO_REJECTED,
            details=audit_details
        )
        db.session.commit()

        return jsonify({
            "message": f"User {user.email} rejected successfully.",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to reject user: {str(e)}"}), 

