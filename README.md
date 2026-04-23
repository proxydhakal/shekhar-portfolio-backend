# Shekhar Portfolio (Backend)

Django-based e-portfolio with dynamic content, blog, contact form, newsletter, and environment-based configuration (local/production).

## Features

- **Portfolio**: Hero, about, skills (Font Awesome), projects, experience, education, certifications
- **Blog**: List/detail, categories, tags, comments, search
- **Contact**: Form with HTML email confirmation; XSS/SQL-injection–aware validation
- **Newsletter**: Subscription with HTML welcome email
- **Admin**: Custom-themed at `/iamadmin/` (not `/admin/`)
- **Theming**: Light/dark mode, Tailwind CSS (built locally), Alpine.js for nav/breadcrumbs
- **Production-ready**: ENVIRONMENT-based settings, MySQL for production, SQLite for local, SMTP/console email, HTTPS & security headers

## Tech Stack

- **Django 5.2 LTS** · Python 3.x
- **Tailwind CSS 3** (npm build)
- **Alpine.js** · Lucide icons · Font Awesome
- **SQLite** (local) / **MySQL** (production)
- **WhiteNoise** (static files in production)

## Project Structure

```
eportfolio_shekhar/
├── apps/
│   ├── portfolio/          # Main site: index, contact, newsletter, profile, projects, etc.
│   │   ├── models.py       # SiteConfiguration, Profile, Skill, Project, Experience, Education, Certification, ContactMessage, NewsletterSubscriber
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py         # '' → index
│   │   ├── templates/      # base.html, portfolio/index.html, portfolio/email/
│   │   └── management/commands/
│   │       └── insert_portfolio_data.py
│   └── blog/
│       ├── models.py       # BlogPost, Comment, Category, Tag
│       ├── views.py        # BlogListView, BlogDetailView
│       ├── urls.py         # '', '<slug>/'
│       └── templates/blog/
├── eportfolio_project/
│   ├── settings/           # Environment-based settings
│   │   ├── __init__.py     # Loads local or production by ENVIRONMENT
│   │   ├── base.py         # Shared settings
│   │   ├── local.py        # DEBUG=True, SQLite, console email
│   │   └── production.py   # DEBUG=False, MySQL, SMTP, security headers
│   ├── urls.py             # iamadmin/, '', blog/
│   └── wsgi.py
├── templates/              # Project-level templates
│   └── admin/              # Themed admin (base, login, base_site)
├── static/
│   ├── css/
│   │   ├── src/input.css   # Tailwind source
│   │   └── dist/output.css # Built CSS (committed)
│   └── images/             # Favicons
├── manage.py
├── requirements.txt
├── package.json            # Tailwind build scripts
├── tailwind.config.js
├── .env.example
└── .gitignore
```

## Prerequisites

- Python 3.10+
- Node.js & npm (for Tailwind)
- MySQL (production only)

## Setup

### 1. Clone and enter project

```bash
git clone https://github.com/proxydhakal/shekhar-portfolio-backend.git
cd shekhar-portfolio-backend
```

### 2. Virtual environment and Python dependencies

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment variables

```bash
cp .env.example .env
# Edit .env: set SECRET_KEY, and for production set ENVIRONMENT=production, ALLOWED_HOSTS, DB_*, EMAIL_*
```

For **local** use default `ENVIRONMENT=local` (SQLite, console email).  
For **production** set `ENVIRONMENT=production` and fill MySQL + SMTP + `ALLOWED_HOSTS`.

### 4. Database

```bash
python manage.py migrate
# Optional: seed data
python manage.py insert_portfolio_data
# Optional: clear and reseed
python manage.py insert_portfolio_data --clear
```

### 5. Tailwind CSS (optional if `static/css/dist/output.css` is present)

```bash
npm install
npm run build:css
# Development with watch:
# npm run watch:css
```

### 6. Run development server

```bash
python manage.py runserver
```

- Site: **http://127.0.0.1:8000/**
- Blog: **http://127.0.0.1:8000/blog/**
- Admin: **http://127.0.0.1:8000/iamadmin/** (not `/admin/`)

## Environment Variables (summary)

| Variable           | Description                    | Local | Production |
|--------------------|--------------------------------|-------|------------|
| `ENVIRONMENT`      | `local` or `production`        | ✓     | ✓         |
| `SECRET_KEY`       | Django secret                  | ✓     | ✓         |
| `ALLOWED_HOSTS`    | Comma-separated hosts          | optional | required |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | MySQL | — | ✓ |
| `EMAIL_FROM`       | Sender for contact/newsletter  | optional | ✓       |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP | — | ✓ |

See `.env.example` for full list and comments.

## Production

- Set `ENVIRONMENT=production` and configure `.env` (ALLOWED_HOSTS, MySQL, SMTP, EMAIL_FROM).
- Install MySQL and `mysqlclient` (included in `requirements.txt`).
- Run migrations, then:
  ```bash
  python manage.py collectstatic --noinput
  ```
- Serve via Gunicorn/uWSGI behind a reverse proxy (HTTPS). Settings enable `SECURE_SSL_REDIRECT`, HSTS, secure cookies, and XSS/clickjacking headers.

## License

Private / All rights reserved.
