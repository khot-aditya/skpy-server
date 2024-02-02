# your_module/__init__.py
from flask import Blueprint

auth = Blueprint("auth", __name__)

messaging = Blueprint("messaging", __name__)
