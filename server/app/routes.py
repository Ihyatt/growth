from app.app import app
from flask import jsonify, abort

@app.route('/api/luna')
def luna():
    try:
        return jsonify(message="Hello, I'm Luna")
    except Exception as e:
        abort(500, description=str(e))


@app.route('/api/romeo')
def romeo():
    try:
        return jsonify(message="Hello, I'm Romeo")
    except Exception as e:
        abort(500, description=str(e))