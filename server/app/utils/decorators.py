# app/utils/auth_decorators.py
from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from app.models.constants.enums import PermissionLevel,ValidationLevel
from sqlalchemy_continuum import transaction_class
from app.models.constants.enums import UserLevel, ApprovalStatus, ProfileStatus


from app.models.medication import Medication
from app.models.report import Report



def enforce_role_admin():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.filter_by(user_id).first()
                
                if not user:
                    return jsonify({"msg": "User not found"}), 404

                if user.permission != PermissionLevel.ADMIN and not user.is_validated == ValidationLevel.APPROVED:
                    return jsonify({"msg": "Access forbidden: Insufficient permissions"}), 403

                if user.is_validated != ValidationLevel.APPROVED:
                    return jsonify({"msg": "Access forbidden: Insufficient validation"}), 403

                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"msg": str(e)}), 401
        return wrapper
    return decorator


def enforce_elite_user():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.filter_by(user_id).first()
            
                if not user:
                    return jsonify({"msg": "User not found"}), 404

                elite_users = [UserLevel.PRACTITIONER, UserLevel.Admin]


                if user.user_level not in elite_users or  and not user.approval_status == ApprovalStatus.APPROVED:
                    return jsonify({"msg": "Access forbidden: Insufficient permissions"}), 403

                if user.approval_status != ApprovalStatus.APPROVED:
                    return jsonify({"msg": "Access forbidden: Insufficient validation"}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"msg": str(e)}), 401
        return wrapper
    return decorator


def enforce_role_patient():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.filter_by(user_id).first()
           
                if not user:
                    return jsonify({"msg": "User not found"}), 404

                if user.user_level != UserLevel.PATIENT:
                    return jsonify({"msg": "you are not a patient"}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"msg": str(e)}), 401
        return wrapper
    return decorator



def set_versioning_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            identity = get_jwt_identity()
            if identity:
                user = User.query.filter_by(id=identity).first()
                if user:
                    transaction_class().user = user
        except Exception:
            pass 
        return fn(*args, **kwargs)
    return wrapper



def get_resource_model(resource_type_str):

    resource_models_map = {
        'medication': Medication,
        'report': Report,
    }
    
    model = resource_models_map.get(resource_type_str.lower())
    
    if not model:
        abort(400, description=f"Invalid resource type: '{resource_type_str}'")
        
    return model
