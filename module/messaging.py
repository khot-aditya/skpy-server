from flask import Blueprint, request, jsonify
from skpy import Skype

messaging = Blueprint("messaging", __name__)

# Initialize Skype client as None
skype_client = None


@messaging.route("/message", methods=["POST"])
def send_message():
    try:
        # Retrieve the username, password, chatId, and message from the request's JSON payload
        data = request.json
        username = data.get("username")
        password = data.get("password")
        to = data.get("to")
        message = data.get("message")

        # Validate required fields
        if not all([username, password, to, message]):
            raise ValueError("Missing required fields")

        file_name = username
        directory_path = "./token/"
        file_path = f"{directory_path}{file_name}.txt"

        # Create a new instance of the Skype client using the provided username, password, and token file
        global skype_client  # Use the global variable
        skype_client = Skype(username, password, file_path)

        # Iterate over each chat ID
        for chat_id in to:
            # Retry sending message up to 3 times
            for _ in range(3):
                try:
                    # Retrieve the contact object corresponding to the chatId from the Skype client's contacts
                    contact_username = chat_id
                    contact = skype_client.contacts[contact_username]

                    # Send the message content to the contact's chat
                    message_content = message
                    contact.chat.sendMsg(message_content)

                    # If message is sent successfully, break out of the retry loop
                    break

                except Exception as e:
                    # Log the error (you can customize this based on your logging setup)
                    print(f"Error sending message to {chat_id}: {str(e)}")

        # Return a JSON response with a status of "success" and a HTTP status code of 200
        return jsonify({"status": "success"}), 200

    except ValueError as ve:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 400
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        # Return a JSON response with a status of "error", the error message as a string, and a HTTP status code of 500
        return jsonify({"status": "error", "message": str(e)}), 500
