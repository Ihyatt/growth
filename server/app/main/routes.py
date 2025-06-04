
from flask import request, jsonify
from app.main import bp
from app.models.user import User
from app.database import db
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from app.models.constants.enums import PermissionLevel,ValidationLevel
from app.utils.auth_decorators import jwt_required_with_role
from app.utils.audit_log import log_audit



@bp.route('/api/login', methods=['POST'])
def login():

    try:
        data = request.get_json()
        print(1)
        username = data.get('username', '').strip()
        password = data.get('password', '') 
        print(2)
        if not username or not password:
            return jsonify(error="Email and password are required."), 400
        print(3)
        user = User.query.filter_by(username=username).first()
        print(4)
        print(user.id, password)
        print(user.check_password(password))
        if not user or not user.check_password(password):
            return jsonify(error="Invalid username or password."),
        print(5)
        jwt_token = create_access_token(identity=str(user.id))
        print('HELLLOOOO')
        return jsonify(
            message=f"Welcome back, {user.username}",
            jwtToken=jwt_token,
            permission=user.permission
        )

    except Exception as e:
        return jsonify(error="Login failed: " + str(e)), 500


@bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        user_type = data.get('userType', '').strip()

        if not all([email, username, password, user_type]):
            return jsonify(error="Email, password, username, and user type are required."), 400

        if user_type not in ['patient', 'practitioner']:
            return jsonify(error="Invalid user type. Must be 'patient' or 'practitioner'."), 400

        if User.query.filter_by(username=username).first():
            return jsonify(error="Username already exists. Please use a different username."), 400

        if User.query.filter_by(email=email).first():
            return jsonify(error="Email already exists. Please use a different email."), 400

        user = User(email=email)
        user.set_password(password)

        user.permission_level = (
            PermissionLevel.PATIENT if user_type == 'patient'
            else PermissionLevel.PRACTITIONER
        )

        db.session.add(user)
        db.session.commit()

        return jsonify(message=f"User registered successfully with email: {email}")

    except Exception as e:
        db.session.rollback()
        return jsonify(error="Registration failed: " + str(e)), 500



@bp.route('/api/admin/users', methods=['GET'])
@jwt_required_with_role()
def get_admin_users():
    try:
        validation_map = {
            'pending': ValidationLevel.PENDING,
            'approved': ValidationLevel.VALIDATED 
        }

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        status_param = request.args.get('status')
        active_param = request.args.get('active')
        email_param = request.args.get('email')
        active = True if active == 'ACTIVE' else False

        query = User.query
        validation_map = {
            'pending': ValidationLevel.PENDING,
            'approved': ValidationLevel.APPROVED
        }

        query = query.filter_by(
            permission=PermissionLevel.PRACTITIONER,
            is_validated=validation_map[status],
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


@bp.route('/api/admin/approve', methods=['POST'])
@jwt_required_with_role()
def approve_user():
    try:
        data = request.get_json()
        user_id = data.get('userId')

        if not user_id:
            return jsonify({"message": "User ID is required."}), 400

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"message": "User not found."}), 404


        if user.is_validated == ValidationLevel.VALIDATED:
            return jsonify({"message": f"User {user.email} is already approved."}),
        
        old_validation_level = user.is_validated

        user.is_validated = ValidationLevel.VALIDATED

        audit_details = {
            'old_validation_level': old_validation_level,
            'new_validation_level': user.is_validated
        }

        log_admin_action(
            target_user_id=user.id,
            action_type=AuditActionType.PRACTITIONER_APPROVED,
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


@bp.route('/api/admin/reject', methods=['POST'])
@jwt_required_with_role()
def reject_user():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        
        if not user_id:
            return jsonify({"message": "User ID is required."}), 400

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"message": "User not found."}), 404

        if user.is_validated == ValidationLevel.REJECTED:
            return jsonify({"message": f"User {user.email} is already rejected."}), 200

        old_validation_level = user.validation_level
        user.validation_level = ValidationLevel.REJECTED

        audit_details = {
            'old_validation_level': old_validation_level,
            'new_validation_level': user.is_validated
        }

        log_admin_action(
            target_user_id=user.id,
            action_type=AuditActionType.PRACTITIONER_REJECTED,
            details=audit_details
        )
        db.session.commit()

        return jsonify({
            "message": f"User {user.email} rejected successfully.",
            "user": user.to_dict() 
        }), 200
   
    except Exception as e:
        db.session.rollback()

        return jsonify({"message": f"Failed to reject user: {str(e)}"}), 500