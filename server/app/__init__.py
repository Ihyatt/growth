import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate

from app.config import Config  # assuming this is your config class

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
        
    from app import database
    database.init_app(app)
    migrate = Migrate(app, database)

    from app.models.user import User
    
    # Register blueprints
    from app.main.routes import bp
    app.register_blueprint(bp)

    print(f"Current ENV: {os.getenv('ENVIRONMENT')}")
    print(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app