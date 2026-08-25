# نظام إدارة الحلقات القرآنية | Quran Study Circle Management System

A Django 5.2 web application for managing Quran study circles (halaqat): teachers, students, weekly attendance, grades, and weekly progress reports. Arabic RTL UI built with Tailwind CSS.

## Features

### Public
- Landing page (`/`) with role-aware navigation (login link, or logout button for signed-in users)

### Administrator (`/administration/`)
- Dashboard with system overview (teachers, halaqat, students, today's absences)
- Full CRUD for teachers — **creating a teacher automatically creates her login account** (username + password set on the same form); deleting a teacher deletes the linked account
- Full CRUD for halaqat and grades (deletes are blocked while dependent records exist, e.g. reports attached to a halaqa)
- Student management: list/search/filter, add, edit, delete (with confirmation page)
- User account management: search, activate/deactivate, guarded delete
- Attendance records: teacher attendance sheet, per-halaqa student attendance history, filterable + paginated record browsers
- Weekly report review: filter by teacher/halaqa, paginated, detail view per report

### Teacher (staff)
- Own dashboard: today's attendance status of her students at a glance
- Student management scoped to her own halaqat only (add/edit/delete her students)
- Daily attendance sheet per halaqa (defaults to "present", editable statuses + notes)
- Weekly progress report submission (on track / advanced / delayed + reason), one row per halaqa per week (resubmission updates the same row)

## Tech Stack

| Layer      | Choice                                        |
|------------|-----------------------------------------------|
| Backend    | Python 3.13, Django 5.2                       |
| Auth       | django-allauth 65 (username login, POST logout) |
| Database   | SQLite                                        |
| Frontend   | Tailwind CSS (CDN) + Cairo font, vanilla JS   |
| Icons      | Inline heroicons SVG partials                 |

## Project Structure

```
halq_management_system/          # repo root
├── core/                        # settings, root urls, wsgi/asgi
│   ├── adapter.py               # allauth adapter (role-based login redirect)
│   ├── access.py                # shared staff_required / superuser_required decorators
│   └── templatetags/            # version-proof pagination helpers
├── halaqs/                      # Halaqa model (+ form used by administration app)
├── teachers/                    # teacher dashboard
├── students/                    # student & grade views/forms (teacher + admin sides)
├── attendances/                 # daily sheets + record browsers
├── reports/                     # weekly report submit/review
├── administration/              # admin dashboard, teachers/halaqat/users management
├── templates/                   # base layouts, per-app pages, partials/icons
├── static/css/style.css
├── docs/                        # user guide (Word document with screenshots)
├── manage.py
└── requirements.txt
```

All internal links use `{% url %}` reversal; route URLs end with a trailing slash. Shared cross-app code lives in the project package (`adapter.py`, `access.py`, `templatetags/`) instead of a dedicated app.

## User Guide

A full Arabic user guide with annotated screenshots for both roles is included: [`docs/دليل استخدام نظام إدارة الحلقات القرآنية.docx`](docs/دليل%20استخدام%20نظام%20إدارة%20الحلقات%20القرآنية.docx)

## Getting Started (Local)

```powershell
# 1. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations (includes grade seeding)
python manage.py migrate

# 4. Create an admin account
python manage.py createsuperuser

# 5. Run
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — log in from the home page. Admins land on `/administration/dashboard/`, teachers on `/teacher/dashboard/`.

> Teachers should normally be created from the admin UI (Teachers → Add), which provisions the login account in one step.

## Environment Variables

| Variable               | Default            | Purpose                                    |
|------------------------|--------------------|--------------------------------------------|
| `DJANGO_SECRET_KEY`    | dev fallback key   | Set a real secret in production            |
| `DJANGO_DEBUG`         | `True`             | Set `False` in production                  |
| `DJANGO_ALLOWED_HOSTS` | `*`                | Comma-separated hosts in production        |

`CSRF_TRUSTED_ORIGINS` includes `*.pythonanywhere.com`; adjust if deploying elsewhere.

## Deployment (PythonAnywhere)

1. Upload the project (or pull from git) into your home directory
2. Create/update the virtualenv from `requirements.txt`
3. Run `python manage.py migrate` and `collectstatic` if needed
4. Point the web app at the WSGI file and your venv
5. In the **WSGI configuration file** (Web tab), make sure the settings module line reads:
   `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')`
6. Set env vars (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=mortooo.pythonanywhere.com`) and **Reload**

## Notes

- Deleting is intentionally conservative: teachers with linked superuser accounts, halaqat with existing reports, etc. show a blocking confirmation instead of cascading silently.
- Attendance rows are auto-created as "present" when a sheet is opened; saving persists only changed entries.
