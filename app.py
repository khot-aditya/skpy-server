# app.py
from flask import Flask
from module.auth import auth
from module.messaging import messaging

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(messaging)

if __name__ == "__main__":
    app.run(debug=True)
