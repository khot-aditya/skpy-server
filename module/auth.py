from flask import Blueprint, request, jsonify, current_app
from skpy import Skype
import os
import jwt
import datetime

auth = Blueprint("auth", __name__)

# Constants
TOKEN_VALIDITY_PERIOD = datetime.timedelta(weeks=1)
TOKEN_DIRECTORY = "./token/"

# Initialize Skype client as None
skype_client = None


def create_skype_client(username, password, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return Skype(username, password, file_path)


def generate_jwt_token(username):
    token_payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + TOKEN_VALIDITY_PERIOD,
    }
    return jwt.encode(
        token_payload, current_app.config["SECRET_KEY"], algorithm="HS256"
    )


@auth.route("/api/login", methods=["POST"])
def login():
    try:
        # Retrieve the username and password from the request's JSON payload
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # Validate required fields
        if not all([username, password]):
            raise ValueError("Missing required fields")

        global skype_client

        file_name = username
        file_path = os.path.join(TOKEN_DIRECTORY, f"{file_name}.txt")

        # Create a new instance of the Skype client using the provided username, password, and token file
        skype_client = create_skype_client(username, password, file_path)

        # Authenticate with Skype and retrieve the authentication token
        token = skype_client.conn.tokens

        if token:
            jwt_token = generate_jwt_token(username)
        else:
            raise ValueError("Login failed")

        # Return a JSON response with a status of "success" and a HTTP status code of 200
        return jsonify({"status": "success", "payload": {"token": jwt_token}}), 200

    except ValueError as ve:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 400
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 500
        return jsonify({"status": "error", "message": str(e)}), 500
