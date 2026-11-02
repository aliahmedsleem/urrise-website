from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class NavigationItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(255), nullable=False, default="#")
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class NewsPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="draft", nullable=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(60), default="layers")
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(255), default="")
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

def seed_navigation():
    if NavigationItem.query.count() == 0:
        for index, (label, url) in enumerate([
            ("Home", "#home"), ("About", "#about"), ("Services", "#services"),
            ("Projects", "#projects"), ("News", "#news"), ("Contact", "#contact")
        ]):
            db.session.add(NavigationItem(label=label, url=url, sort_order=index))
        db.session.commit()
