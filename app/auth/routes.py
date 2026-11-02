import os
from flask import render_template, request, redirect, url_for, flash, session
from app.auth import bp
from app import db
from app.models import AdminUser

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.clear()
            session["admin_id"] = user.id
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("admin/login.html")

@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@bp.cli.command("create-admin")
def create_admin():
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD")
    if not password or password == "change-this-before-first-run":
        raise SystemExit("Set a strong ADMIN_PASSWORD in environment before creating admin.")
    if AdminUser.query.filter_by(username=username).first():
        raise SystemExit("Admin username already exists.")
    user = AdminUser(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f"Administrator '{username}' created.")
