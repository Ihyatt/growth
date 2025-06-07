from flask import request, jsonify
from app.routes.report import report_bp
from app.models.user import Report, User, ReportComment
from app.database import db
from server.app.utils.decorators import,set_versioning_user
from flask_jwt_extended import get_jwt_identity
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user, set_versioning_user


@report_bp.route('/', methods=['GET'])
def get_report(report_id):
    report =  Report.query.filter_by(report_id).first()
    return jsonify({"medication": report.to_dict()})
    

@report_bp.route('/delete', methods=['POST'])
def delete_report(report_id):
    report_id = request.args.get('report_id')
    report = Report.query.filter_by(report_id).first()
    report_id.is_active = False
    db.session.commit()


@report_bp.route('/create', methods=['POST'])
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