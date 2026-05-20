from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json
import os
from schulmanager import *

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/api/table", methods=["POST"])
def table():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing JSON body"
        }), 400

    jwt_token = data.get("jwt")
    user = data.get("user")

    if not jwt_token or not user:
        return jsonify({
            "error": "Missing 'jwt' or 'user'"
        }), 400

    subjects = Schulmanager(user, jwt_token)
    subjects.init_timetable()
    return jsonify(subjects.get_timetable_json())

if __name__ == "__main__":
    app.run(debug=True)