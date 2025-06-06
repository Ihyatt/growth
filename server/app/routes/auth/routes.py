
from flask import request, jsonify
from app.routes.auth import auth_bp
from app.models.user import User
from app.database import db
from flask_jwt_extended import create_access_token
from app.models.constants.enums import PermissionLevel


@auth_bp.route('/login', methods=['POST'])
def login():

    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '') 
        if not username or not password:
            return jsonify(error="Email and password are required."), 400
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify(error="Invalid username or password."),
        jwt_token = create_access_token(identity=str(user.id))
        print(user.username)
        return jsonify(
            message=f"Welcome back, {user.username}",
            jwtToken=jwt_token,
            permission=user.permission,
            username= user.username
        )

    except Exception as e:
        return jsonify(error="Login failed: " + str(e)), 500


@auth_bp.route('/register', methods=['POST'])
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

