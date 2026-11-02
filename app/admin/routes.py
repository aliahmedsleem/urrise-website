from functools import wraps
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
    return render_template("admin/dashboard.html", counts={"news": NewsPost.query.count(), "services": Service.query.count(), "projects": Project.query.count(), "navigation": NavigationItem.query.count()})

@bp.route("/navigation", methods=["GET", "POST"])
@admin_required
def navigation():
    if request.method == "POST":
        label = request.form.get("label", "").strip()
        url = request.form.get("url", "").strip()
        if label and url:
            db.session.add(NavigationItem(label=label, url=url, sort_order=NavigationItem.query.count()))
            db.session.commit()
            flash("Navigation tab added.", "success")
        return redirect(url_for("admin.navigation"))
    items = NavigationItem.query.order_by(NavigationItem.sort_order).all()
    return render_template("admin/navigation.html", items=items)

@bp.post("/navigation/<int:item_id>/delete")
@admin_required
def delete_navigation(item_id):
    item = db.session.get(NavigationItem, item_id)
    if item:
        db.session.delete(item); db.session.commit(); flash("Tab deleted.", "success")
    return redirect(url_for("admin.navigation"))

@bp.route("/news", methods=["GET", "POST"])
@admin_required
def news():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip().lower()
        summary = request.form.get("summary", "").strip()
        body = request.form.get("body", "").strip()
        status = request.form.get("status", "draft")
        if title and slug and summary and body and status in ("draft", "published"):
            from datetime import datetime, timezone
            post = NewsPost(title=title, slug=slug, summary=summary, body=body, status=status, published_at=datetime.now(timezone.utc) if status == "published" else None)
            db.session.add(post); db.session.commit(); flash("News post saved.", "success")
        else:
            flash("Complete all fields with a valid status.", "error")
        return redirect(url_for("admin.news"))
    posts = NewsPost.query.order_by(NewsPost.created_at.desc()).all()
    return render_template("admin/news.html", posts=posts)
