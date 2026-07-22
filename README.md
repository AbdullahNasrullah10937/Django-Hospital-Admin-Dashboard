# BP Hospitals – Admin Management System

A professional-level hospital administration web application built with Python, Django, HTML5, CSS3, Tailwind CSS / Bootstrap 5 design components, and the Model-View-Template (MVT) architecture.

---

## Project Overview

The **BP Hospitals – Admin Management System** is a centralized administrative portal engineered for managing healthcare networks, hospital facilities, medical directors, and hospital wards.

The application is structured into three separate Django applications:

1. **`hospitals`**: Manages hospital entity records (Name, Location, Founded Year).
2. **`directors`**: Manages hospital director records (Name, Qualification, OneToOne Hospital Assignment).
3. **`wards`**: Manages ward records (Name, Capacity, ForeignKey Hospital Assignment).

---

## Key Features

- **Custom Admin Dashboard**: Real-time summary statistics for Total Hospitals, Total Directors, and Total Wards with recent activity tracking.
- **Complete CRUD Operations**: Full Create, Read (List & Detail), Update, and Delete operations for all entities using Django Class-Based Views (CBVs).
- **Strict Database & Model Constraints**:
  - **Hospital**: Unique hospital names (`unique=True`), realistic founded year bounds (1800 to current year), DB-level `CheckConstraint`.
  - **Director**: Mandatory `OneToOneField` with `on_delete=CASCADE`, `clean()` validation ensuring names are non-numeric and non-empty.
  - **Ward**: Mandatory `ForeignKey` to Hospital (`on_delete=CASCADE`), capacity range validation (1 to 500 beds), DB-level `CheckConstraint`.
- **Search & Pagination**: Live search by name, location, qualification, or hospital assignment with multi-page navigation.
- **Django Admin Panel Integration**: Customized `list_display`, `search_fields`, and `list_filter` in `/admin/`.
- **Authentication & Security**: Restricted views requiring admin authentication (`LoginRequiredMixin`), flash notifications for user actions.
- **Clinical Precision UI/UX**: Custom responsive layout with corporate modern aesthetics, Material Symbols icons, and color tokens.

---

## Setup & Running Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

Access the custom admin application at `http://127.0.0.1:8000/` and the built-in Django Admin interface at `http://127.0.0.1:8000/admin/`.

---

## Explanation of Django Migrations

### What Are Django Migrations?
In Django, **migrations** are Python files that represent changes to database models over time. They serve as a version-control system for database schemas, enabling developers to modify Python data models (`models.py`) and propagate those changes reliably into database tables (such as SQLite, MySQL, or PostgreSQL).

### How Django's Migration System Works
1. **`python manage.py makemigrations`**: Django inspects your application models (`models.py`), compares them against existing migration files, and generates new, milestone migration scripts inside each app's `migrations/` folder (e.g., `0001_initial.py`).
2. **`python manage.py migrate`**: Django executes pending migration scripts against the configured database, creating tables, primary keys, foreign keys, unique indexes, and check constraints (`CheckConstraint`).
3. **Schema Tracking (`django_migrations` table)**: Django creates an internal system table named `django_migrations` inside the database. Each time a migration script is applied, Django records the app name, migration name, and timestamp. When `migrate` runs, Django queries `django_migrations` to determine which migrations have already been executed, preventing redundant schema modifications.

---

## Project Structure

```
BP_Hospitals/
├── BP_Hospitals/             # Main Project Configuration
│   ├── settings.py           # Explicit settings (INSTALLED_APPS, DATABASES, TEMPLATES, STATIC)
│   ├── urls.py               # Main URL routing (Admin, Auth, Dashboard, Apps)
│   ├── wsgi.py
│   └── asgi.py
├── hospitals/                # Hospitals App
│   ├── models.py             # Hospital model & constraints
│   ├── views.py              # Hospital CRUD Views & DashboardView
│   ├── forms.py              # HospitalForm
│   ├── admin.py              # HospitalAdmin registration
│   ├── urls.py               # Hospital URLs
│   └── templates/hospitals/  # Hospital templates
├── directors/                # Directors App
│   ├── models.py             # HospitalDirector model & constraints
│   ├── views.py              # Director CRUD Views
│   ├── forms.py              # DirectorForm
│   ├── admin.py              # HospitalDirectorAdmin registration
│   ├── urls.py               # Director URLs
│   └── templates/directors/  # Director templates
├── wards/                    # Wards App
│   ├── models.py             # Ward model & constraints
│   ├── views.py              # Ward CRUD Views
│   ├── forms.py              # WardForm
│   ├── admin.py              # WardAdmin registration
│   ├── urls.py               # Ward URLs
│   └── templates/wards/      # Ward templates
├── templates/                # Global Layout Templates (base.html, dashboard.html, login.html)
├── manage.py
├── requirements.txt
└── README.md
```
