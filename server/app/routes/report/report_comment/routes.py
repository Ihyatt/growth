from flask import request, jsonify
from app.routes.report.report_comment import report_comment_bp
from app.database import db
from server.app.models.form_template import User, ReportComment

from flask_jwt_extended import get_jwt_identity, jwt_required


@report_comment_bp.route('/create', methods=['POST'])
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


@report_comment_bp.route('/delete', methods=['POST'])
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