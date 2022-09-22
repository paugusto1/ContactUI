from flask import Flask
from config import Config
from flask_cors import CORS
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
csrf = CSRFProtect()
csrf.init_app(app)

from app import routes