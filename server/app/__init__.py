import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.config import Config  # assuming this is your config class

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register extensions after app is created
    from app import database
    database.init_app(app)

    CORS(app)

    # Register blueprints
    from app.main.routes import bp
    app.register_blueprint(bp)

    print(f"Current ENV: {os.getenv('ENVIRONMENT')}")
    print(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app