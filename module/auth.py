# your_module/auth.py
from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return "Login Page"
