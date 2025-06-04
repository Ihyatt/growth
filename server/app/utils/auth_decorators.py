# app/utils/auth_decorators.py
from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from app.models.constants.enums import PermissionLevel,ValidationLevel


def jwt_required_with_role():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(user_id)

                if not user:
                    return jsonify({"msg": "User not found"}), 404

                if user.permission != PermissionLevel.ADMIN and not user.is_validated == ValidationLevel.APPROVED:
                    return jsonify({"msg": "Access forbidden: Insufficient permissions"}), 403

                if user.is_validated != ValidationLevel.APPROVED:
                    return jsonify({"msg": "Access forbidden: Insufficient validation"}), 403

                g.user_id = user.id 
                g.user_role = user.permission 
                g.user_validation = user.is_validated
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"msg": str(e)}), 401
        return wrapper
    return decorator