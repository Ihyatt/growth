from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app import database
from app.routes import bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.routes.auth.routes import auth_bp
from app.routes.admins.routes import admins_bp
from app.routes.therapists.routes import therapists_bp
from app.routes.patients.routes import patients_bp

from app.config import Config



def create_app():

    load_dotenv()

    jwt = JWTManager()

    app = Flask(__name__)

    CORS(app)
    
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admins_bp)
    app.register_blueprint(therapists_bp)
    app.register_blueprint(patients_bp)

    database.init_app(app)
    Migrate(app, database.db)
    
    app.config["JWT_SECRET_KEY"] = "romeoluna" 
    jwt.init_app(app)

    app.register_blueprint(bp, url_prefix='/api')
    
    print(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app