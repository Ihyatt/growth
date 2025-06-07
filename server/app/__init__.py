
import logging
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app import database
from app.routes import bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.routes.auth.routes import auth_bp
from app.routes.admin.routes import admin_bp
from app.routes.practitioners.routes import practitioner_bp
from app.routes.patient.routes import patient_bp

from app.config import Config



def create_app():
    app = Flask(__name__)
    load_dotenv()

    jwt = JWTManager()

    
    log_level = os.environ.get('FLASK_LOG_LEVEL', 'INFO').upper()
    log_file_path = os.environ.get('FLASK_LOG_FILE', 'application.log')

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(), # Console output
            logging.FileHandler(log_file_path) # File output
        ]
    )

    app.logger.setLevel(log_level)
    app.logger.info("Application starting up and logging configured.")


    CORS(app)
    
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(practitioner_bp)
    app.register_blueprint(patient_bp)

    database.init_app(app)
    Migrate(app, database.db)
    
    app.config["JWT_SECRET_KEY"] = "romeoluna" 
    jwt.init_app(app)

    app.register_blueprint(bp, url_prefix='/api')
    
    print(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app