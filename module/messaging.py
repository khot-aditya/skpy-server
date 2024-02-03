from flask import Blueprint, request, jsonify, current_app
from skpy import Skype
import jwt
import os

messaging = Blueprint("messaging", __name__)

# Constants
MAX_RETRY_ATTEMPTS = 3
TOKEN_DIRECTORY = "./token/"

# Initialize Skype client as None
skype_client = None


def initialize_skype_client(token):
    decoded_token = jwt.decode(
        token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
    )
    username = format(decoded_token["username"])

    file_name = username
    file_path = os.path.join(TOKEN_DIRECTORY, f"{file_name}.txt")

    global skype_client  # Use the global variable
    skype_client = Skype(None, None, file_path)


def send_message_to_contact(contact, message_content):
    contact.chat.sendMsg(message_content)


@messaging.route("/api/message", methods=["POST"])
def send_message():
    try:
        token = request.headers.get("Authorization")
        # Retrieve the chatId, and message from the request's JSON payload
        data = request.json
        to = data.get("to")
        message = data.get("message")

        # Validate required fields
        if not all([to, message]):
            raise ValueError("Missing required fields")

        try:
            initialize_skype_client(token)

            # Iterate over each chat ID
            for chat_id in to:
                # Retry sending message up to MAX_RETRY_ATTEMPTS times
                for _ in range(MAX_RETRY_ATTEMPTS):
                    try:
                        contact_username = chat_id
                        contact = skype_client.contacts[contact_username]

                        send_message_to_contact(contact, message)

                        # If message is sent successfully, break out of the retry loop
                        break

                    except Exception as e:
                        print(f"Error sending message to {chat_id}: {str(e)}")

            # Return a JSON response with a status of "success" and a HTTP status code of 200
            return jsonify({"status": "success"}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

    except ValueError as ve:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 400
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 500
        return jsonify({"status": "error", "message": str(e)}), 500
