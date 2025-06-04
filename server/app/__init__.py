from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app import database
from app.main import bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta


from app.config import Config

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
        
    database.init_app(app)
    Migrate(app, database.db)
    
    app.config["JWT_SECRET_KEY"] = "romeoluna" 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt.init_app(app)


    from app.models.user import User
    
    app.register_blueprint(bp)

    print(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app