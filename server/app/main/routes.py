from flask import request, jsonify
from app.main import bp
from app.models.user import User
from app.database import db
from flask_jwt_extended import create_access_token
from app.models.model_enums import PermissionLevel


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

        jwt_token = create_access_token(identity=user.id)
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
