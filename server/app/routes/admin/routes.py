import logging

from flask import request, jsonify
from app.routes.admin.routes import admin_bp
from server.app.models.form_template import User
from app.database import db
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.app.utils.helpers import audit_log_helper,get_current_user_object,resource_owner_or_admin_required, roles_required, care_giver_or_admin_required
from app.utils.helpers import audit_log_helper
from app.models.constants.enums import UserLevel, UserApprovalStatus, ProfileStatus, AuditActionStatus
from server.app.utils.decorators import enforce_role_admin, set_versioning_user
from flask_jwt_extended import get_jwt_identity


logger = logging.getLogger(__name__)


user_approval_status_map = {
    'PENDING': UserApprovalStatus.PENDING,
    'APPROVED': UserApprovalStatus.APPROVED,
    'REJECTED': UserApprovalStatus.REJECTED, 
}

user_level_status_map = {
    'PATIENT': UserLevel.PATIENT,
    'PRACTITIONER': UserLevel.PRACTITIONER,
    'ADMIN': UserLevel.ADMIN, 
}

profile_status_map = {
    'ACTIVE': ProfileStatus.ACTIVE,
    'INACTIVE': ProfileStatus.INACTIVE,
}


@admin_bp.route('/search', methods=['GET'])
def get_users():
    try:
        user_approval_status_map = {
            'PENDING': UserApprovalStatus.PENDING,
            'APPROVED': UserApprovalStatus.APPROVED,
            'REJECTED': UserApprovalStatus.REJECTED, 
        }

        user_level_status_map = {
            'PATIENT': UserLevel.PATIENT,
            'PRACTITIONER': UserLevel.PRACTITIONER,
            'ADMIN': UserLevel.ADMIN, 
        }

        profile_status_map = {
            'ACTIVE': ProfileStatus.ACTIVE,
            'INACTIVE': ProfileStatus.INACTIVE,
        }

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        user_status_param = request.args.get('status')
        profile_status_param = request.args.get('active')
        email_param = request.args.get('email')
        username_param = request.args.get('username')
        user_level_param = request.args.get('user_level')
        
        query = User.query
        query = query.filter_by(
            approval_status=user_approval_status_map[user_status_param],
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


@admin_bp.route('/approve-practioner/<int:user_id>', methods=['POST'])
def approve_practioners(user_id):
    try:
        admin_id = get_jwt_identity()
        user_id = request.args.get('user_id')

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

        audit_log_helper(
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


@admin_bp.route('/reject-practitioner/<int:user_id>', methods=['POST'])
def reject_practioners():
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({"message": "User ID is required."}), 400

        user = User.query.filter_by(id=user_id).first()

        if user.user_level != UserLevel.PRACTITIONER:
            return jsonify({'message': 'user is not a practioner'}), 404

        if not user:
            return jsonify({"message": "User not found."}), 404


        if user.approval_status == UserApprovalStatus.REJECTED:
            return jsonify({"message": f"User {user.email} is already rejected."}),
        
        old_validation_level = user.is_validated

        user.approval_status = UserApprovalStatus.REJECTED

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
        return jsonify({"message": f"Failed to reject user: {str(e)}"})
    


@admin_bp.route('/actvate/<int:user_id>', methods=['POST'])
def activate_account(user_id):
    try:

        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({"message": "User not found."}), 404

        if user.profile_status == ProfileStatus.ACTIVE:
            return jsonify({'message': 'user is already active'}), 404

        old_activation_status = user.profile_status

        user.profile_status = ProfileStatus.ACTIVE

        audit_details = {
            'old_activation_status': old_activation_status,
            'new_activation_status': user.profile_status
        }

        log_audit(
            target_user_id=user.id,
            action_type=AuditActionStatus.SET_TO_ACTIVE,
            details=audit_details
        )

        db.session.commit()

        return jsonify({
            "message": f"User {user.email} to to inactive successfully.",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to deactive user: {str(e)}"})
    



@admin_bp.route('/deactivate/<int:user_id>', methods=['POST'])
def deactivate_account(user_id):
    try:

        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({"message": "User not found."}), 404

        if user.profile_status == ProfileStatus.INACTIVE:
            return jsonify({'message': 'user is already deactivated'}), 404

        old_activation_status = user.profile_status

        user.profile_status = ProfileStatus.INACTIVE

        audit_details = {
            'old_activation_status': old_activation_status,
            'new_activation_status': user.profile_status
        }

        log_audit(
            target_user_id=user.id,
            action_type=AuditActionStatus.SET_TO_INACTIVE,
            details=audit_details
        )
        db.session.commit()

        return jsonify({
            "message": f"User {user.email} to to inactive successfully.",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to deactive user: {str(e)}"})
    


@admin_bp.route('/search-practitioners', methods=['GET'])
@jwt_required()
@roles_required([UserLevel.ADMIN])
def search_practitioners():
    try:
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)

        practitioners_query = User.query.filter_by(user_level=UserLevel.PRACTITIONER)

        user_status_param = request.args.get('status')
        if user_status_param:
            mapped_status = user_approval_status_map.get(user_status_param.upper())
            if mapped_status is None:
                return jsonify(message=f"Invalid 'status' parameter: {user_status_param}"), 400
            practitioners_query = practitioners_query.filter_by(approval_status=mapped_status)

        profile_status_param = request.args.get('active')
        if profile_status_param is not None:
            mapped_profile_status = profile_status_map.get(str(profile_status_param).lower())
            if mapped_profile_status is None:
                 return jsonify(message=f"Invalid 'active' parameter: {profile_status_param}"), 400
            practitioners_query = practitioners_query.filter_by(profile_active=mapped_profile_status) # Assuming 'profile_active' is the field name

        email_param = request.args.get('email')
        if email_param:
            practitioners_query = practitioners_query.filter_by(email=email_param)

        username_param = request.args.get('username')
        if username_param:
            practitioners_query = practitioners_query.filter_by(username=username_param)

        users_pagination = practitioners_query.paginate(page=page, per_page=limit, error_out=False)


        return jsonify({
            "users": [user.to_dict() for user in users_pagination.items],
            "total": users_pagination.total,
            "page": users_pagination.page,
            "pages": users_pagination.pages,
            "has_next": users_pagination.has_next,
            "has_prev": users_pagination.has_prev
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error searching practitioners: {e}")
        db.session.rollback()
        return jsonify(error="An unexpected error occurred: " + str(e)),



@admin_bp.route('/search-patients', methods=['GET'])
@jwt_required()
@roles_required([UserLevel.ADMIN]) # Only admins can search practitioners
def search_patients():
    try:
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)

        practitioners_query = User.query.filter_by(user_level=UserLevel.PATIENT)

        profile_status_param = request.args.get('active')
        if profile_status_param is not None:
            mapped_profile_status = profile_status_map.get(str(profile_status_param).lower())
            if mapped_profile_status is None:
                 return jsonify(message=f"Invalid 'active' parameter: {profile_status_param}"), 400
            practitioners_query = practitioners_query.filter_by(profile_active=mapped_profile_status) # Assuming 'profile_active' is the field name

        email_param = request.args.get('email')
        if email_param:
            practitioners_query = practitioners_query.filter_by(email=email_param)

        username_param = request.args.get('username')
        if username_param:
            practitioners_query = practitioners_query.filter_by(username=username_param)

        users_pagination = practitioners_query.paginate(page=page, per_page=limit, error_out=False)


        return jsonify({
            "users": [user.to_dict() for user in users_pagination.items],
            "total": users_pagination.total,
            "page": users_pagination.page,
            "pages": users_pagination.pages,
            "has_next": users_pagination.has_next,
            "has_prev": users_pagination.has_prev
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error searching patients: {e}")
        db.session.rollback()
        return jsonify(error="An unexpected error occurred: " + str(e)),




@admin_bp.route('/search-admins', methods=['GET'])
@jwt_required()
@roles_required([UserLevel.ADMIN])
def search_practitioners():
    try:
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)

        practitioners_query = User.query.filter_by(user_level=UserLevel.ADMIN)

        user_status_param = request.args.get('status')
        if user_status_param:
            mapped_status = user_approval_status_map.get(user_status_param.upper())
            if mapped_status is None:
                return jsonify(message=f"Invalid 'status' parameter: {user_status_param}"), 400
            practitioners_query = practitioners_query.filter_by(approval_status=mapped_status)

        profile_status_param = request.args.get('active')
        if profile_status_param is not None:
            mapped_profile_status = profile_status_map.get(str(profile_status_param).lower())
            if mapped_profile_status is None:
                 return jsonify(message=f"Invalid 'active' parameter: {profile_status_param}"), 400
            practitioners_query = practitioners_query.filter_by(profile_active=mapped_profile_status)

        email_param = request.args.get('email')
        if email_param:
            practitioners_query = practitioners_query.filter_by(email=email_param)

        username_param = request.args.get('username')
        if username_param:
            practitioners_query = practitioners_query.filter_by(username=username_param)

        users_pagination = practitioners_query.paginate(page=page, per_page=limit, error_out=False)


        return jsonify({
            "users": [user.to_dict() for user in users_pagination.items],
            "total": users_pagination.total,
            "page": users_pagination.page,
            "pages": users_pagination.pages,
            "has_next": users_pagination.has_next,
            "has_prev": users_pagination.has_prev
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error searching practitioners: {e}")
        db.session.rollback()
        return jsonify(error="An unexpected error occurred: " + str(e)),

