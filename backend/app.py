from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
import os
from email_service import send_email
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, get_auth_url, get_token

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Handle File Upload
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    df = pd.read_excel(filepath) if file.filename.endswith(".xlsx") else pd.read_csv(filepath)
    return jsonify({"columns": df.columns.tolist(), "data": df.to_dict(orient="records")})

# Handle Email Sending
@app.route("/send_email", methods=["POST"])
def send_email_route():
    data = request.json
    recipient = data.get("recipient")
    subject = data.get("subject")
    body = data.get("body")

    if not recipient or not subject or not body:
        return jsonify({"error": "Missing email details"}), 400

    send_email(recipient, subject, body)
    return jsonify({"success": "Email sent successfully!"})

# Microsoft OAuth Login
@app.route("/login")
def login():
    return redirect(get_auth_url())

@app.route("/callback")
def callback():
    token = get_token(request.args.get("code"))
    session["token"] = token
    return redirect(url_for("index"))

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
