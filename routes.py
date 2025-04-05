from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db import db, User
from job_matching import process_resume
import os
from config import UPLOAD_FOLDER

def register_routes(app):
    
    # Ensure a secret key is set for session management
    app.secret_key = "supersecretkey"
    @app.route('/reupload')
    def reupload():
        return render_template('dashboard.html')
    @app.route('/dashboard')
    def dashboard():
        if "user_id" in session:
            user = User.query.get(session["user_id"])
            return render_template('dashboard.html', full_name=user.full_name)
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            full_name = request.form["full_name"]
            email = request.form["email"]
            password = generate_password_hash(request.form["password"], method="pbkdf2:sha256")

            if User.query.filter_by(email=email).first():
                flash("Email already exists!", "danger")
                return redirect(url_for("register"))

            new_user = User(full_name=full_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html")
     
    @app.route("/feedback")
    def about_tool():
        return render_template("feedback.html")
    
    @app.route("/version")
    def techstack():
        return render_template("version.html")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id  # Store user ID in session
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid email or password", "danger")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("user_id", None)  # Remove user from session
        flash("Logged out successfully!", "info")
        return redirect(url_for("login"))

    @app.route("/upload", methods=["POST"])
    def upload_resume():
        try:
            if "resume" not in request.files:
                return jsonify({"error": "No file uploaded"}), 400

            file = request.files["resume"]
            if not file.filename.endswith(".pdf"):
                return jsonify({"error": "Only PDF resumes are allowed"}), 400

            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            result = process_resume(filepath)
            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
