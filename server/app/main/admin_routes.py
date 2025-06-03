from flask import request, jsonify
from app.main import bp
from app.models.user import User
from app.database import db
from flask_jwt_extended import create_access_token
from app.models.model_enums import PermissionLevel


# @bp.route('admin/therapists/', methods=['GET'])
# def get_pending_therapists():

#     therapists = User.query.filter_by(permission=PermissionLevel.PRACTITIONER, is_approved=False).all()
#     return jsonify([t.to_dict() for t in therapists])

# @bp.route('admin/therapists/<int:user_id>', methods=['GET'])
# def get_pending_therapists():
#     # Example assumes unapproved therapists have a field like `is_approved = False`
#     therapists = User.query.filter_by(permission=PermissionLevel.PRACTITIONER, is_approved=False).all()
#     return jsonify([t.to_dict() for t in therapists])

# @bp.route('admin/therapists/<int:user_id>/approve', methods=['POST'])
# def approve_therapist(user_id):
#     user = User.query.get(user_id)
#     if not user or user.permission != PermissionLevel.PRACTITIONER:
#         return jsonify(error="Invalid therapist ID"), 404

#     user.is_approved = True
#     db.session.commit()
#     return jsonify(message=f"Therapist {user.username} approved")

# @bp.route('admin/therapists/<int:user_id>/reject', methods=['POST'])
# def reject_therapist(user_id):
#     user = User.query.get(user_id)
#     if not user or user.permission != PermissionLevel.PRACTITIONER:
#         return jsonify(error="Invalid therapist ID"), 404

#     db.session.delete(user)
#     db.session.commit()
#     return jsonify(message=f"Therapist {user.username} rejected and removed")