# your_module/messaging.py
from flask import Blueprint

messaging = Blueprint("messaging", __name__)

@messaging.route("/message")
def send_message():
    return "Send Message Page"
