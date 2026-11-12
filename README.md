# Forest Fire Detection System

A fully functional, web-based **Forest Fire Detection and Monitoring System** built with Python Django. This academic project demonstrates real-time sensor data processing, fire risk assessment, alert generation, and incident management for forest fire scenarios.

---

## Project Objectives

- Continuously monitor forest environmental conditions via sensor nodes
- Detect fire risk conditions (Normal → Warning → Fire Suspected → Fire Detected)
- Generate and manage alerts with email/SMS notification support
- Track fire incidents with full CRUD and history
- Provide role-based access for Administrators, Forest Officers, Fire Department, and Local Authorities
- Visualize data with interactive charts, statistics, and a Leaflet map

---

## Technologies Used

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.14, Django 6.1.2 |
| Database | SQLite (default), PostgreSQL-ready |
| Frontend | HTML5, Bootstrap 5.3, Bootstrap Icons |
| Charts | Chart.js 4.4 |
| Maps | Leaflet 1.9 + OpenStreetMap (free, no API key) |
| Forms | django-crispy-forms + crispy-bootstrap5 |
| Auth | Django built-in + CustomUser with roles |
| Config | python-dotenv (.env file) |
| Email | Django console backend (configurable SMTP) |

---

## Project Structure

```
Forest fire DS/
├── manage.py
├── db.sqlite3              # SQLite database
├── .env                    # Environment variables (not committed)
├── .env.example            # Template for production
├── requirements.txt
├── README.md
├── forest_fire/            # Django project config
│   ├── settings.py
│   └── urls.py
├── accounts/               # User auth & roles (Module 9)
├── forest_env/             # Forest/area/weather (Modules 1, 8)
├── sensors/                # Sensor nodes & readings (Modules 2, 3)
├── detection/              # Risk assessment & thresholds (Modules 4, 5, 6)
├── alerts/                 # Alert & notification (Module 7)
├── incidents/              # Fire incidents (Modules 10, 12)
├── response_mgmt/          # Emergency response (Module 11)
├── reports/                # Dashboard & reports (Module 13)
├── core/                   # Management commands, context processors
├── static/                 # CSS & JS
└── templates/              # HTML templates
```

---

## Modules Implemented

| # | Module | Status |
|---|--------|--------|
| 1 | Forest Environment (Forest, Area, Vegetation, Wildlife, Weather) | ✅ Complete |
| 2 | Sensor Module (Temperature, Smoke, Flame, Humidity, Gas, Node) | ✅ Complete |
| 3 | Data Collection (Sensor readings, timestamps) | ✅ Complete |
| 4 | Data Processing (Validation, Fusion, Thresholds) | ✅ Complete |
| 5 | Fire Detection (Normal/Warning/Suspected/Detected states) | ✅ Complete |
| 6 | Fire Risk Assessment (Per-sensor + overall risk scoring) | ✅ Complete |
| 7 | Alert & Notification (Email/SMS/Mobile - configurable) | ✅ Complete |
| 8 | Location & Monitoring (GPS coords, forest zones) | ✅ Complete |
| 9 | Authority & User (Roles: Admin, Officer, Fire Dept, Local) | ✅ Complete |
| 10 | Fire Incident Management (CRUD + updates + history) | ✅ Complete |
| 11 | Response & Management (Emergency, Suppression, Evacuation) | ✅ Complete |
| 12 | Historical Data (Sensor history, incident records) | ✅ Complete |
| 13 | Reporting & Visualization (Dashboard, Charts, Map, Reports) | ✅ Complete |

---

## Installation Instructions

### Prerequisites

- Python 3.10+ (tested with Python 3.14.5)
- pip

### Step 1 — Clone / Download the project

Place the project folder on your machine. The root contains `manage.py`.

### Step 2 — Create a virtual environment (recommended)

```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies

```cmd
python -m pip install -r requirements.txt
```

### Step 4 — Configure environment variables

Copy `.env.example` to `.env` and edit as needed:

```cmd
copy .env.example .env
```

Default `.env` settings work out-of-the-box for local development (SQLite + console email).

### Step 5 — Run database migrations

```cmd
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Create an administrator account

**Option A — Use the demo data seed (recommended for demo/academic use):**

```cmd
python manage.py seed_demo_data
```

This creates the following accounts (all passwords are shown):

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator (superuser) |
| officer | demo1234 | Forest Officer |
| fireofficer | demo1234 | Fire Department |
| localadmin | demo1234 | Local Authority |
| sysadmin | demo1234 | Administrator |

> ⚠️ All sensor readings created by `seed_demo_data` are **SIMULATED** and not real measurements.

**Option B — Create only a superuser manually:**

```cmd
python manage.py createsuperuser
```

---

## Starting the Django Development Server

```cmd
python manage.py runserver
```

---

## Accessing the Website

Open your browser and go to:

```
http://127.0.0.1:8000/
```

- **Login page:** `http://127.0.0.1:8000/accounts/login/`
- **Dashboard:** `http://127.0.0.1:8000/dashboard/`
- **Admin panel:** `http://127.0.0.1:8000/admin/`

---

## Demo Data Instructions

Run the seed command to populate all demo data:

```cmd
python manage.py seed_demo_data
```

This creates:
- 3 Forests with 6 Forest Areas (including GPS coordinates)
- 6 Sensor Nodes (one per area, with all 5 sensor sub-types)
- 120 Sensor Readings across 4 scenarios (Normal, Warning, Fire Suspected, Fire Detected)
- 6 Weather condition records
- 3 Fire Incidents (past events)
- 5 Alerts at various severity levels

To re-run the seed (it skips duplicates automatically):

```cmd
python manage.py seed_demo_data
```

---

## Email Notification Setup (Optional)

By default, email output goes to the server console. To enable real email alerts:

Edit `.env`:

```ini
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

---

## SMS Notification Setup (Optional)

SMS integration is implemented as a mock/demo by default. To enable Twilio SMS:

Edit `.env`:

```ini
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
```

---

## Key URLs Summary

| URL | Description |
|-----|-------------|
| `/` | Redirects to Dashboard |
| `/accounts/login/` | Login page |
| `/accounts/register/` | Registration |
| `/dashboard/` | Main dashboard |
| `/dashboard/fire-risk-map/` | Leaflet map |
| `/dashboard/alert-history/` | Full alert log |
| `/dashboard/incident-reports/` | Incident report |
| `/dashboard/statistical-reports/` | Statistics |
| `/forest/` | Forest list |
| `/forest/areas/` | Forest areas |
| `/sensors/` | Sensor nodes |
| `/sensors/readings/` | All readings |
| `/detection/` | Risk assessment |
| `/detection/status/` | Live detection status |
| `/alerts/` | Alert management |
| `/incidents/` | Fire incidents |
| `/response/` | Emergency response |
| `/admin/` | Django admin panel |

---

## Running Tests

```cmd
python manage.py test
```

---

## License

Academic project — for educational/demonstration purposes only.
