from flask import request, jsonify
from app.routes.report import report_bp
from app.models.user import Report
from app.database import db
from server.app.utils.decorators import,set_versioning_user
from flask_jwt_extended import get_jwt_identity
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user, set_versioning_user

@report_bp.route('/search', methods=['GET'])
@set_versioning_user
@enforce_elite_user
def get_patients_reports():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    username = request.args.get('username')
    
    query = Report.query

    query = query.filter_by(practitioner_id=current_user_id,)

    if username:
        query = query.filter(Report.patient_username.ilike(f'%{username}%'))

    query = query.order_by(Report.created_at.desc())
    
    reports_pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "forms": [report.to_dict() for report in reports_pagination.items],
        "total": reports_pagination.total,
        "page": reports_pagination.page,
        "pages": reports_pagination.pages,
        "has_next": reports_pagination.has_next,
        "has_prev": reports_pagination.has_prev,
    })

@report_bp.route('<str:username>/report/<int:report_id>', methods=['GET'])
@set_versioning_user
@enforce_elite_user
def get_report():
    report_id = request.args.get('report_id')
    report_id = request.args.get('report_id')
    report =  Report.query.filter_by(report_id).first()


    return jsonify({"medication": report.to_dict()})
    

@report_bp.route('/<str:username>/report/<int:report_id>/delete', methods=['POST'])
@set_versioning_user
@enforce_elite_user
def delete_report():
    practitioner_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')
    report_id = request.args.get('report_id')

    medication = Report.query.filter_by(report_id).first()
    report_id.is_active = False
    db.session.commit()