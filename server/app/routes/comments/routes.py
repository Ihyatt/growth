
from flask import request, jsonify
from app.routes.comments import comments_bp
from server.app.models.patient_form import Comment
from app.database import db
from app.utils.decorators import get_resource_model
from flask_jwt_extended import get_jwt_identity, jwt_required


@comments_bp.route('/create/<string:resource_type>', methods=['POST'])
@jwt_required()
def create():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('text')
    resource_type = request.args.get('resource_type')


    resource_model = get_resource_model(resource_type) #error handle here

    new_comment = Comment(
        text=comment_text,
        user_id=current_user_id,
        resource_type=resource_model.lower(), 
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

    ResourceModel = get_resource_model(resource_type)

    resource_instance = ResourceModel.query.filter_by(resource_id).first()

    # put logic that checks instance

    new_comment = Comment(
        text=comment_text,
        user_id=current_user_id,
        resource_type=resource_type.lower(),
        resource_id=resource_instance.id   
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201