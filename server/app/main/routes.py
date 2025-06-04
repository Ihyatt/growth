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
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify(error="Username and password are required."), 400

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify(error="Invalid username or password."), 401

        jwt_token = create_access_token(identity=str(user.id))
        return jsonify(
            message=f"Welcome back, {username}",
            jwtToken=jwt_token,
            permission=user.permission
        )

    except Exception as e:
        return jsonify(error="Login failed: " + str(e)), 500


@bp.route('/api/register', methods=['POST'])
def register():
    try:

        data = request.get_json()
        print(data)
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        user_type = data.get('userType', '').strip()

        if not all([username, email, password, user_type]):
            return jsonify(error="All fields are required."), 400

        if user_type not in ['patient', 'practitioner']:
            return jsonify(error="Invalid user type."), 400

        if User.query.filter_by(email=email).first():
            return jsonify(error="User already exists."), 400

        print('passed all conditionals')
        user = User(username=username, email=email)
        user.set_password(password)
        user.permission = (
            PermissionLevel.PATIENT if user_type == 'patient'
            else PermissionLevel.PRACTITIONER
        )

        db.session.add(user)
        db.session.commit()

        return jsonify(message=f"User {username} registered successfully")

    except Exception as e:
        db.session.rollback()
        return jsonify(error="Registration failed: " + str(e)), 500




@bp.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_admin_users():
    current_user = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    status = request.args.get('status')
    active = request.args.get('active')
    email = request.args.get('email')
    active = True if active == 'active' else False
    print("Authorization Header:", request.headers.get('Authorization'))

    query = User.query


    if status == 'pending':
        if email:
            query = query.filter_by(
                permission=PermissionLevel.PRACTITIONER,
                is_validated=ValidationLevel.PENDING,
                email=email
            )
        else:
            query = query.filter_by(
                permission=PermissionLevel.PRACTITIONER,
                is_validated=ValidationLevel.PENDING, 
                is_active=active
            )
    elif status == 'approved':
        if email:
            query = query.filter_by(
                permission=PermissionLevel.PRACTITIONER,
                is_validated=ValidationLevel.PENDING,
                email=email
            )
        else:
            query = query.filter_by(
                permission=PermissionLevel.PRACTITIONER,
                is_validated=ValidationLevel.APPROVED, 
                is_active=active
            )

    users = query.paginate(page=page, per_page=limit, error_out=False)
    

    return jsonify({
        "users": [user.to_dict() for user in users.items],
        "total": users.total,
        "page": users.page,
        "pages": users.pages,
        "has_next": users.has_next,
        "has_prev": users.has_prev
    })


@bp.route('/api/admin/approve', methods=['POST'])
@jwt_required_with_role()
def approve_user():
    current_user = get_jwt_identity()
    data = request.get_json()
    user_id = data.get('userId')
    user = User.query.filter_by(id=user_id).first()
    details = {
        'before': user.is_validated,
        'after': ValidationLevel.APPROVED
    }
    user.is_validated = ValidationLevel.APPROVED
    
    try:

        log_audit(
            user_id,
            'approve',
            details,
            'user'
        )
        db.session.commit()
        return jsonify({
            "message": f"User  approved successfully.",
            "user": user.to_dict()
        }), 200
   
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to approve user : {str(e)}"}), 500


@bp.route('/api/admin/reject', methods=['POST'])
@jwt_required_with_role()
def reject_user():
    current_user = get_jwt_identity()
    data = request.get_json()
    user_id = data.get('userId')
    user = User.query.filter_by(id=user_id).first()
    details = {
        'before': user.is_validated,
        'after': ValidationLevel.REJECTED
    }
    user.is_validated = ValidationLevel.REJECTED

    try:
        
        log_audit(
            user_id,
            'reject',
            details,
            'user'
        )
        db.session.commit()
        return jsonify({
            "message": f"User  reject successfully.",
            "user": user.to_dict()
        }), 200
   
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": f"Failed to reject user : {str(e)}"}), 500
