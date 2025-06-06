from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app import database
from app.routes import bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Import top-level blueprints
from app.routes.auth.routes import auth_bp
from app.routes.admin.routes import admin_bp
from app.routes.forms.routes import forms_bp
from app.routes.medications.routes import medications_bp
from app.routes.reports.routes import reports_bp


from app.config import Config

load_dotenv()

jwt = JWTManager()

app = Flask(__name__)

def create_app():
    
    app.config.from_object(Config)


    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admins')
    app.register_blueprint(medications_bp, url_prefix='/medications')
    app.register_blueprint(forms_bp, url_prefix='/forms')
    app.register_blueprint(reports_bp, url_prefix='/reports')


    from app.routes.admin.routes import admin_bp
    from app.routes.forms.routes import forms_bp
    from app.routes.medications.routes import medications_bp
    from app.routes.reports.routes import reports_bp
    
    CORS(app)
        
    database.init_app(app)
    Migrate(app, database.db)
    
    app.config["JWT_SECRET_KEY"] = "romeoluna" 
    jwt.init_app(app)


    
    app.register_blueprint(bp, url_prefix='/api')
    

    print(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app