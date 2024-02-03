from flask import Blueprint, request, jsonify
from skpy import Skype
import os

auth = Blueprint("auth", __name__)

# Initialize Skype client as None
skype_client = None


@auth.route("/login", methods=["POST"])
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
        directory_path = "./token/"

        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        file_path = f"{directory_path}{file_name}.txt"

        # Create a new instance of the Skype client using the provided username, password, and token file
        skype_client = Skype(username, password, file_path)  # Authenticate with Skype
        # token = skype_client.conn.tokens  # Retrieve the authentication token

        # Return a JSON response with a status of "success" and a HTTP status code of 200
        return jsonify({"status": "success", "payload": {"username": username}}), 200

    except ValueError as ve:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 400
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 500
        return jsonify({"status": "error", "message": str(e)}), 500
