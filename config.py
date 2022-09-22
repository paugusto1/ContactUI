import os
from flask_wtf import CSRFProtect

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password_contacts_api'