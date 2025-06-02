from app.main import bp
from flask import jsonify, abort

from app.main import bp

@bp.route('/api/login', methods=['POST'])
def login():
    try:
        return jsonify(message="Hello, I'm Luna")
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/api/register', methods=['POST'])
def register():
    try:
        return jsonify(message="Hello, I'm Romeo")
    except Exception as e:
        abort(500, description=str(e))