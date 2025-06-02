from flask import Flask
from flask_cors import CORS
from app.config import Config
from flask import Blueprint

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

from app.main import routes