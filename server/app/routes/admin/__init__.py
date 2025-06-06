from flask import Blueprint
from app.routes.admins import admins_bp
from app.routes.auth import auth_bp
from app.routes.forms import forms_bp
from app.routes.medications import medications_bp
from app.routes.reports import reports_bp

# Create a list of blueprints to register in the app
blueprints = [admins_bp, auth_bp, forms_bp, medications_bp, reports_bp]