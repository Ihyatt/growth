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
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify(error="User not found"), 404

        if user and not user.check_password(password):
            return jsonify(error="Invalid password"), 404

        access_token = create_access_token(identity=user.id)
        return jsonify(message=f"welcome back, {name}", access_token=access_token)
    except Exception as e:
        print("Invalid login", e)
        return jsonify(error=str(e)), 500


@bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(data)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('userType')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify(error="User already exists"), 400

        user = User(username=name, email=email)
        user.set_password(password)
        
        if user_type == 'patient':
            user.permission = PermissionLevel.PATIENT
        
        if user_type == 'practitioner':
            user.permission = PermissionLevel.PRACTITIONER


        db.session.add(user)
        db.session.commit()

        return jsonify(message=f"User {name} registered successfully")
    except Exception as e:
        db.session.rollback()
        print("Error saving user:", e)
        return jsonify(error=str(e)), 500
    