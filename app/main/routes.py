from flask import render_template, abort
from app.main import bp
from app.models import NavigationItem, Service, Project, NewsPost

@bp.get("/")
def index():
    navigation = NavigationItem.query.filter_by(is_active=True).order_by(NavigationItem.sort_order).all()
    services = Service.query.filter_by(is_active=True).order_by(Service.sort_order).all()
    projects = Project.query.filter_by(is_active=True).order_by(Project.sort_order).all()
    news = NewsPost.query.filter_by(status="published").order_by(NewsPost.published_at.desc()).limit(3).all()
    return render_template("main/index.html", navigation=navigation, services=services, projects=projects, news=news)

@bp.get("/news/<slug>")
def news_detail(slug):
    post = NewsPost.query.filter_by(slug=slug, status="published").first_or_404()
    return render_template("main/news_detail.html", post=post)
