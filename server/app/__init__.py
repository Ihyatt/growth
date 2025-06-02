from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app import database
from app.main.routes import bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


from app.config import Config

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
        
    database.init_app(app)
    Migrate(app, database.db)
    
    app.config["JWT_SECRET_KEY"] = "romeoluna" 

    JWTManager(app)

    from app.models.user import User
    
    app.register_blueprint(bp)

    print(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app