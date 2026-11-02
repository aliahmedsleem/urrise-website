from functools import wraps
from datetime import datetime, timezone
from flask import render_template, request, redirect, url_for, flash, session
from app.admin import bp
from app import db
from app.models import AdminUser, NavigationItem, NewsPost, Service, Project

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id") or not db.session.get(AdminUser, session["admin_id"]):
            session.clear()
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

@bp.get("/")
@admin_required
def dashboard():
    counts = {"news": NewsPost.query.count(), "services": Service.query.count(), "projects": Project.query.count(), "navigation": NavigationItem.query.count()}
    return render_template("admin/dashboard.html", counts=counts)

@bp.route("/navigation", methods=["GET", "POST"])
@admin_required
def navigation():
    if request.method == "POST":
        label, url = request.form.get("label", "").strip(), request.form.get("url", "").strip()
        if label and url:
            db.session.add(NavigationItem(label=label, url=url, sort_order=NavigationItem.query.count()))
            db.session.commit(); flash("Navigation tab added.", "success")
        else: flash("Label and URL are required.", "error")
        return redirect(url_for("admin.navigation"))
    items = NavigationItem.query.order_by(NavigationItem.sort_order).all()
    return render_template("admin/navigation.html", items=items)

@bp.post("/navigation/<int:item_id>/delete")
@admin_required
def delete_navigation(item_id):
    item = db.session.get(NavigationItem, item_id)
    if item: db.session.delete(item); db.session.commit(); flash("Tab deleted.", "success")
    return redirect(url_for("admin.navigation"))

@bp.route("/news", methods=["GET", "POST"])
@admin_required
def news():
    if request.method == "POST":
        title, slug = request.form.get("title", "").strip(), request.form.get("slug", "").strip().lower()
        summary, body = request.form.get("summary", "").strip(), request.form.get("body", "").strip()
        status = request.form.get("status", "draft")
        exists = NewsPost.query.filter_by(slug=slug).first()
        if title and slug and summary and body and status in ("draft", "published") and not exists:
            post = NewsPost(title=title, slug=slug, summary=summary, body=body, status=status, published_at=datetime.now(timezone.utc) if status == "published" else None)
            db.session.add(post); db.session.commit(); flash("News post saved.", "success")
        else: flash("Complete fields, choose valid status, and use a unique slug.", "error")
        return redirect(url_for("admin.news"))
    posts = NewsPost.query.order_by(NewsPost.created_at.desc()).all()
    return render_template("admin/news.html", posts=posts)

@bp.route("/services", methods=["GET", "POST"])
@admin_required
def services():
    if request.method == "POST":
        title, description = request.form.get("title", "").strip(), request.form.get("description", "").strip()
        if title and description:
            db.session.add(Service(title=title, description=description, sort_order=Service.query.count()))
            db.session.commit(); flash("Service added.", "success")
        else: flash("Title and description are required.", "error")
        return redirect(url_for("admin.services"))
    items = Service.query.order_by(Service.sort_order).all()
    return render_template("admin/services.html", items=items)

@bp.post("/services/<int:item_id>/delete")
@admin_required
def delete_service(item_id):
    item = db.session.get(Service, item_id)
    if item: db.session.delete(item); db.session.commit(); flash("Service deleted.", "success")
    return redirect(url_for("admin.services"))

@bp.route("/projects", methods=["GET", "POST"])
@admin_required
def projects():
    if request.method == "POST":
        title, description = request.form.get("title", "").strip(), request.form.get("description", "").strip()
        url = request.form.get("url", "").strip()
        if title and description:
            db.session.add(Project(title=title, description=description, url=url, sort_order=Project.query.count()))
            db.session.commit(); flash("Project added.", "success")
        else: flash("Title and description are required.", "error")
        return redirect(url_for("admin.projects"))
    items = Project.query.order_by(Project.sort_order).all()
    return render_template("admin/projects.html", items=items)

@bp.post("/projects/<int:item_id>/delete")
@admin_required
def delete_project(item_id):
    item = db.session.get(Project, item_id)
    if item: db.session.delete(item); db.session.commit(); flash("Project deleted.", "success")
    return redirect(url_for("admin.projects"))
