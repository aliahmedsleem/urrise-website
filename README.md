# URRISE Technologies — Official Website

Official corporate website and CMS for URRISE Technologies, built with Flask.

## Features in this initial foundation

- Navy and gold responsive corporate landing page
- Dynamic navigation tabs
- News creation with draft/published status and public article pages
- Services and projects management
- Protected admin dashboard with CSRF protection
- SQLite database initialization and seed navigation
- Password hashing for administrator accounts

## Stack

Python 3.11+, Flask, Flask-SQLAlchemy, Flask-WTF, Jinja2, SQLite, Nginx, Gunicorn.

## Local setup (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set a long random `SECRET_KEY` and a strong `ADMIN_PASSWORD`. Do not commit `.env`.

Create the administrator:

```powershell
$env:SECRET_KEY="your-long-random-secret"
$env:ADMIN_USERNAME="admin"
$env:ADMIN_PASSWORD="replace-with-a-strong-password"
flask --app run.py auth create-admin
```

Start the development server:

```powershell
py run.py
```

Public website: `http://127.0.0.1:5050`
Admin login: `http://127.0.0.1:5050/admin/login`

## Production notes

- Use a dedicated virtual environment and Gunicorn service.
- Set `SECRET_KEY`, `DATABASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` through a protected environment file.
- Enable HTTPS at Nginx and set secure session cookies behind TLS.
- Keep the SQLite database and uploads outside Git.
- This initial CMS has create/delete flows for content; editing existing items, media uploads, and richer page builder features are planned next.

## Repository

`https://github.com/aliahmedsleem/urrise-website`
