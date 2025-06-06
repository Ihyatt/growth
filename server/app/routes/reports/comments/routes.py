
from flask import request, jsonify
from app.routes.reports.comments import medication_comments_bpcomments_bp
from app.database import db
from app.models.user import User, ReportComment

from flask_jwt_extended import get_jwt_identity, jwt_required


@medication_comments_bpcomments_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('text')

    new_comment = ReportComment(
        text=comment_text,
        user_id=current_user_id,
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201


@medication_comments_bpcomments_bp.route('<int:comment_id>/edit', methods=['POST'])
@jwt_required()
def edit():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_id = request.args.get('comment_id')
    comment_text = data.get('text')


    medication_comment = ReportComment.query.filter_by(comment_id).first()
    medication_comment.text = comment_text
    db.session.commit()

    return jsonify({'success': 'success'}), 201