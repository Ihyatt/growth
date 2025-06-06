
from flask import request, jsonify
from app.routes.comments import comments_bp
from app.models.user_form import UserForm, User, PractitionerForm, Comment
from app.database import db
from server.app.routes.helpers.model_helpers import get_resource_model
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.constants.enums import FormStatus, FormResponses
from server.app.utils.decorators import enforce_role_practioner, enforce_role_patient, enforce_role_practioner, set_versioning_user
from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType #this needs to be set up for permissions, or actually i can use a decoratore


@comments_bp.route('/create/<string:resource_type>', methods=['POST'])
@jwt_required()
def create():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('text')
    resource_type = request.args.get('resource_type')

    new_comment = Comment(
        text=comment_text,
        user_id=current_user_id,
        resource_type=resource_type.lower(), 
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201


@comments_bp.route('edit/<string:resource_type>/<int:resource_id>', methods=['POST'])
@jwt_required()
def edit():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('text')
    resource_type = request.args.get('resource_type')
    resource_id = request.args.get('resource_id')

    # ResourceModel = get_resource_model(resource_type)

    # resource_instance = ResourceModel.query.get(resource_id)

    # put logic that checks instance

    new_comment = Comment(
        text=comment_text,
        user_id=current_user_id,
        resource_type=resource_type.lower(),
        resource_id=resource_id   
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201