

import json
import logging
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.database import db
from app.models.audit_log import AuditLog, User, CareTeam
from app.models.constants.enums import AuditActionType, UserLevel

from functools import wraps
from flask import jsonify, g




logger = logging.getLogger(__name__)

def get_current_user_object():
    try:
        current_user_id = get_jwt_identity()
        if current_user_id is None:
            logger.warning("get_jwt_identity returned None despite @jwt_required passing. Unexpected.")
            return None

        user = User.query.get(current_user_id) 

        if user is None:
            logger.warning(f"User with ID {current_user_id} from JWT not found in database.")
            return None

        return user
    except Exception as e:

        logger.exception(f"Unexpected error retrieving current user object for ID {get_jwt_identity()}: {e}")
        return None #
    

def audit_log_helper(
    admin_id: admin_id,
    audited_id: int,
    action_type: AuditActionType.APPROVED,
    details: dict = None
    ):
    
    try:
        new_log = AuditLog(
            admin_id=admin_id,
            audited_id=audited_id,
            action_type=action_type,
            details=details
        )
        db.session.add(new_log)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback() 


def resource_owner_or_admin_required(username_param_name: str):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            current_user = get_current_user_object()

            if not current_user:
                logger.warning("Authorization failed: No authenticated user object found for a protected resource.")
                return jsonify({"message": "Unauthorized: Authentication required or user profile invalid."}), 401

            target_username = kwargs.get(username_param_name)

            if target_username is None:
                logger.error(f"Decorator misconfiguration: '{username_param_name}' not found in route arguments.")
                return jsonify({"message": "Server error: Resource identifier missing."}), 500


            if current_user.user_level == UserLevel.ADMIN:
                logger.debug(f"Access granted: Admin '{current_user.username}' accessing resource for '{target_username}'.")
                return fn(*args, **kwargs)

            if current_user.username == target_username:
                logger.debug(f"Access granted: User '{current_user.username}' accessing their own resource.")
                return fn(*args, **kwargs)
            else:
                logger.warning(f"Access denied: User '{current_user.username}' (level: {current_user.user_level.name}) attempted to access resource for '{target_username}'.")
                return jsonify({"message": "Forbidden: You do not have permission to access this resource."}), 403

        return decorator
    return wrapper



def roles_required(roles: list[UserLevel]): # Added type hint for clarity

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_current_user_object()

            if not current_user:
                logger.warning("Authorization failed (roles_required): No authenticated user object found.")
                return jsonify({"message": "Unauthorized: Authentication required or user profile invalid."}), 401

            if current_user.user_level in roles:
                logger.debug(f"Access granted: User '{current_user.username}' (level: {current_user.user_level.name}) has a required role.")
                return fn(*args, **kwargs)
            else:
                logger.warning(
                    f"Access denied: User '{current_user.username}' (level: {current_user.user_level.name}) "
                    f"does not have any of the required roles: {[role.name for role in roles]}."
                )
                return jsonify({"message": "Forbidden: You do not have permission to access this resource."}), 403

        return decorator
    return wrapper



def care_giver_or_admin_required(username_param_name: str):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            current_user = get_current_user_object()

            if not current_user:
                logger.warning("Authorization failed: No authenticated user object found for a protected resource.")
                return jsonify({"message": "Unauthorized: Authentication required or user profile invalid."}), 401

            target_username = kwargs.get(username_param_name)

            if target_username is None:
                logger.error(f"Decorator misconfiguration: '{username_param_name}' not found in route arguments.")
                return jsonify({"message": "Server error: Resource identifier missing."}), 500


            patient_user = User.query.filter_by(username=target_username).first()

            if not patient_user:
                logger.warning(f"Patient user '{target_username}' not found.")
                return jsonify({"message": "User not found."}), 404

            
            patient_caregiver = CareTeam.query.filter_by(patient_id=patient_user.id, practitioner_id=current_user.id).first()

            if current_user.user_level == UserLevel.ADMIN or (current_user.user_level == UserLevel.PRACTITIONER and patient_caregiver != None):
                logger.debug(f"Access granted: {current_user.user_level} '{current_user.username}' accessing resource for '{target_username}'.")
                return fn(*args, **kwargs)

            logger.warning(f"Access denied: User '{current_user.username}' (level: {current_user.user_level.name}) attempted to access resource for '{target_username}'.")
            return jsonify({"message": "Forbidden: You do not have permission to access this resource."}), 403

        return decorator
    return wrapper
