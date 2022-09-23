from flask import Flask
from config import Config
from flask_cors import CORS
from flask_wtf import CSRFProtect

application = Flask(__name__)

if __name__ == "__main__":
    application.run(ssl_context='adhoc')

application.config.from_object(Config)
CORS(application)
csrf = CSRFProtect()
csrf.init_app(application)

from app import routes