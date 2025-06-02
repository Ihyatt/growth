from app.main import bp
from flask import request, jsonify, abort
from app.models.user import User
from app.database import db
from flask_jwt_extended import create_access_token
from app.models.model_enums import PermissionLevel

from app.main import bp

@bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(data)
        username = data.get('username').strip()
        password = data.get('password').strip()
        user = User.query.filter_by(username=username).first()

        if not user:
            print("User not found")
            return jsonify(error="User not found"), 404

        if user and not user.check_password(password):
            print("Invalid password")
            return jsonify(error="Invalid password"), 404

        jwt_token = create_access_token(identity=user.id)
        return jsonify(message=f"welcome back, {username}", jwtToken=jwt_token, permission=user.permission)
    
    except Exception as e:
        print("Invalid login", e)
        return jsonify(error=str(e)), 500


@bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username').strip()
        email = data.get('email').strip()
        password = data.get('password').strip()
        user_type = data.get('userType').strip()

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify(error="User already exists"), 400

        user = User(username=username, email=email)
        print('error in login', user)
        user.set_password(password)
        
        if user_type == 'patient':
            user.permission = PermissionLevel.PATIENT
        
        if user_type == 'practitioner':
            user.permission = PermissionLevel.PRACTITIONER


        db.session.add(user)
        db.session.commit()

        return jsonify(message=f"User {username} registered successfully")
    except Exception as e:
        db.session.rollback()
        print("Error saving user:", e)
        return jsonify(error=str(e)), 500
    