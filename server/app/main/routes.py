from app.main import bp
from flask import request, jsonify, abort
from app.models.user import User
from app.database import db

from app.main import bp

@bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')  # Password checking later

        # Lookup user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify(error="User not found"), 404

        # (Add real password check here if stored)
        return jsonify(message=f"Welcome back, {user.username}")
    except Exception as e:
        abort(500, description=str(e))


@bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify(error="User already exists"), 400

        user = User(username=name, email=email)
        user.set_password(password)  # <-- hash & set the password_hash here

        db.session.add(user)
        db.session.commit()

        return jsonify(message=f"User {name} registered successfully")
    except Exception as e:
        db.session.rollback()
        print("Error saving user:", e)
        return jsonify(error=str(e)), 500