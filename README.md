# نظام إدارة الحلقات القرآنية | Quran Study Circle Management System

A Django 5.2 multi-school web application for managing Quran study circles (halaqat): teachers, students, weekly attendance, grades, and weekly progress reports. Arabic RTL UI built with Tailwind CSS.

## Features

### Public Landing Page (`/`)
- Role-aware navigation (login, register school, download APK)
- Feature showcase and role descriptions
- Direct APK download for mobile app

### Multi-School Architecture
- Each school operates as an isolated tenant — teachers, students, halaqat, grades, and attendance are all scoped to a single school
- Three user roles: **Global Admin** (manages schools), **School Admin** (manages their school), **Teacher** (manages their halaqat)

### School Registration (`/schools/register/`)
- One-step registration: create a school + admin account in a single form
- Auto-login after registration, redirects to school admin dashboard

### Global Admin (`/schools/`) — superuser without a school
- List all schools with teacher/student/halaqa counts
- Create, edit, deactivate, and delete schools
- Assign/remove superusers to schools

### School Admin (`/administration/`) — superuser with a school
- Dashboard with system overview (teachers, halaqat, students, today's absences)
- Full CRUD for teachers — **creating a teacher automatically creates her login account** (username + password set on the same form); deleting a teacher deletes the linked account
- Full CRUD for halaqat and grades (deletes are blocked while dependent records exist)
- Student management: list/search/filter, add, edit, delete (with confirmation page)
- User account management: search, activate/deactivate, guarded delete
- Attendance records: teacher attendance sheet, per-halaqa student attendance history, filterable + paginated record browsers
- Weekly report review: filter by teacher/halaqa, paginated, detail view per report

### Teacher (staff) — linked to a teacher record
- Own dashboard: today's attendance status of her students at a glance
- Student management scoped to her own halaqat only (add/edit/delete her students)
- Daily attendance sheet per halaqa (defaults to "present", editable statuses + notes)
- Weekly progress report submission (on track / advanced / delayed + reason), one row per halaqa per week (resubmission updates the same row)

## Tech Stack

| Layer      | Choice                                             |
|------------|----------------------------------------------------|
| Backend    | Python 3.13, Django 5.2                            |
| Auth       | django-allauth 65 (username login, POST logout)    |
| Database   | SQLite                                             |
| Frontend   | Tailwind CSS (local) + Cairo font, vanilla JS      |
| Icons      | Inline heroicons SVG partials                      |
| Mobile     | Android APK download served from `/download-apk/`  |

## Project Structure

```
halq_management_system/          # repo root
├── core/                        # settings, root urls, wsgi/asgi
│   ├── adapter.py               # allauth adapter (role-based login redirect)
│   ├── access.py                # staff_with_school / superuser_with_school decorators
│   ├── middleware.py             # SchoolMiddleware — sets request.school per user
│   └── templatetags/            # version-proof pagination helpers
├── schools/                     # School + UserProfile models, register school flow
├── halaqs/                      # Halaqa model (+ form used by administration app)
├── teachers/                    # teacher dashboard
├── students/                    # student & grade views/forms (teacher + admin sides)
├── attendances/                 # daily sheets + record browsers
├── reports/                     # weekly report submit/review
├── administration/              # admin dashboard, teachers/halaqat/users management
├── templates/                   # base layouts, per-app pages, partials/icons
│   ├── schools/                 # school management templates (g_base, list, form, register)
│   ├── administration/          # admin sidebar (s_base), CRUD pages
│   ├── teachers/                # teacher sidebar (t_base), dashboard
│   └── account/                 # login, signup, password reset
├── static/
│   ├── css/style.css            # design system (tokens, components)
│   └── vendor/tailwind.js       # local Tailwind CSS build
├── إدارة الحلقات.apk            # Android APK for download
├── docs/                        # user guide (Word document with screenshots)
├── manage.py
└── requirements.txt
```

## User Roles & Access

| Role | How created | Login redirects to | Can access |
|------|-------------|-------------------|------------|
| **Global Admin** | `createsuperuser` (no school profile) | `/schools/` | `/schools/*` only |
| **School Admin** | Register school flow or assigned via `/schools/` users page | `/administration/dashboard/` | `/administration/*`, teacher/student/attendance/report pages |
| **Teacher** | Created by school admin from Teachers → Add | `/teacher/dashboard/` | Own dashboard, own students, own attendance, weekly reports |

## User Guide

A full Arabic user guide with annotated screenshots is included: [`docs/دليل استخدام نظام إدارة الحلقات القرآنية.docx`](docs/دليل%20استخدام%20نظام%20إدارة%20الحلقات%20القرآنية.docx)

## Getting Started (Local)

```powershell
# 1. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations (includes grade seeding + school data migration)
python manage.py migrate

# 4. Create an admin account
python manage.py createsuperuser

# 5. Run
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — register a new school from the home page, or log in with an existing account.

> Teachers should normally be created from the school admin UI (Teachers → Add), which provisions the login account in one step.

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
3. Run `python manage.py migrate` and `python manage.py collectstatic --noinput`
4. Point the web app at the WSGI file and your venv
5. In the **WSGI configuration file** (Web tab), make sure the settings module line reads:
   `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')`
6. Set env vars (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=mortooo.pythonanywhere.com`) and **Reload**

## Notes

- **Multi-tenant isolation**: All views, forms, and queries are filtered by `request.school` set via `SchoolMiddleware`. Users only see data belonging to their school.
- Deleting is intentionally conservative: teachers with linked superuser accounts, halaqat with existing reports, etc. show a blocking confirmation instead of cascading silently.
- Attendance rows are created on POST (not auto-created on page load); saving persists only changed entries.
- The APK download is served from `/download-apk/` — place the APK file in the project root directory.
- Signal auto-creates `UserProfile` for non-superuser users only; superusers get profiles when assigned to a school.
