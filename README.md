# 🎉 EventMaster — Event Management System

A full-stack **Django** web application for discovering, creating, and managing events. Built with a role-based access system for Admins, Organizers, and Participants — deployed on Vercel.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-eventmanagement--pink.vercel.app-blueviolet?style=flat-square&logo=vercel)](https://eventmanagement-pink.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.1-green?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)

---

## 🌐 Live Demo

👉 **[https://eventmanagement-pink.vercel.app/](https://eventmanagement-pink.vercel.app/)**

---

## ✨ Features

### 👤 Role-Based Access Control
Three distinct user roles with tailored experiences:
- **Admin** — Full platform control, user management, event oversight
- **Organizer** — Create, edit, and manage their own events; view registrations
- **Participant** — Browse events, RSVP, manage their registrations via a personal dashboard

### 📅 Event Management
- Create and manage events with title, description, date, location, and cover image
- Browse a public event listing page accessible without login
- Event detail pages with full information

### ✅ RSVP & Registration
- One-click event registration for participants
- Instant email confirmation on successful RSVP
- View and manage personal registrations from a smart dashboard

### 📊 Smart Dashboards
- Organizer dashboard to track events and attendee counts
- Participant dashboard to view upcoming and past registrations

### 🖼️ Media & Storage
- Cloudinary integration for event cover image uploads
- WhiteNoise for efficient static file serving

### 📧 Email Notifications
- SMTP-based email system (Gmail) for registration confirmations and updates

### 🗄️ Database
- PostgreSQL via Supabase for scalable, cloud-hosted data storage

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Django 6.0.1 |
| Database | PostgreSQL (Supabase, via `psycopg2-binary`) |
| Frontend Styling | Tailwind CSS 3.4 (compiled via PostCSS) |
| Templating | Django Templates (HTML) |
| Media Storage | Cloudinary |
| Static Files | WhiteNoise |
| Email | Gmail SMTP |
| Deployment | Vercel (Python serverless) |
| Config | python-decouple |
| Dev Tools | Django Debug Toolbar, Faker (for seed data) |

---

## 📁 Project Structure

```
EventMaster---Event-management-system/
├── core/                   # Core app (homepage, shared views/templates)
├── event_management/       # Django project settings, wsgi.py, urls.py
├── events/                 # Event models, views, URLs, templates
├── users/                  # User registration, login, profile, roles
├── media/                  # Uploaded media files (local dev)
├── static/
│   └── css/
│       ├── tailwind.css    # Tailwind source
│       └── output.css      # Compiled CSS
├── staticfiles/            # Collected static files for deployment
├── manage.py
├── populate_db.py          # Script to seed the database with fake data
├── reset_db.py             # Script to reset the database
├── requirements.txt
├── package.json            # Tailwind CSS build scripts
├── tailwind.config.js
├── vercel.json             # Vercel deployment config
└── .env                    # Environment variables (see note below)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js (for Tailwind CSS compilation)
- PostgreSQL database (local or Supabase)
- Cloudinary account

### 1. Clone the repository

```bash
git clone https://github.com/naim13107/EventMaster---Event-management-system.git
cd EventMaster---Event-management-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Node dependencies (for Tailwind)

```bash
npm install
```

### 5. Set up environment variables

Create a `.env` file in the project root (never commit this to GitHub):

```env
SECRET_KEY=your-django-secret-key

# Database (PostgreSQL / Supabase)
host=your-db-host
port=5432
dbname=postgres
user=your-db-user
password=your-db-password

# Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 6. Compile Tailwind CSS

```bash
# One-time build
npm run build:tailwind

# Watch mode during development
npm run watch:tailwind
```

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. (Optional) Seed the database with sample data

```bash
python populate_db.py
```

### 9. Create a superuser

```bash
python manage.py createsuperuser
```

### 10. Start the development server

```bash
python manage.py runserver
```

The app will be at `http://127.0.0.1:8000/`

---

## 🗂️ Pages & Routes

| URL | Description |
|---|---|
| `/` | Home — platform overview and features |
| `/events/event-list/` | Public event listing — browse all events |
| `/events/<id>/` | Event detail page |
| `/users/sign-up/` | User registration |
| `/users/sign-in/` | User login |
| `/users/dashboard/` | Participant dashboard — my RSVPs |
| `/users/organizer-dashboard/` | Organizer dashboard — manage events |
| `/admin/` | Django admin panel |

---

## 👥 User Roles

| Role | Capabilities |
|---|---|
| **Admin** | Full access — manage all users, events, and registrations via Django admin |
| **Organizer** | Create & manage own events, view participant lists |
| **Participant** | Browse events, RSVP, manage registrations from personal dashboard |

---

## 📜 Available Scripts

| Command | Description |
|---|---|
| `python manage.py runserver` | Start local Django development server |
| `npm run build:tailwind` | Compile Tailwind CSS to `output.css` |
| `npm run watch:tailwind` | Watch and auto-recompile Tailwind CSS |
| `python populate_db.py` | Seed database with sample events and users |
| `python reset_db.py` | Reset (clear) the database |
| `python manage.py collectstatic` | Collect static files for deployment |

---

## ☁️ Deployment (Vercel)

This project runs as a Django serverless app on Vercel using the `@vercel/python` builder.

```json
{
  "builds": [{
    "src": "event_management/wsgi.py",
    "use": "@vercel/python",
    "config": { "maxLambdaSize": "15mb", "runtime": "python3.11.3" }
  }],
  "routes": [{ "src": "/(.*)", "dest": "event_management/wsgi.py" }]
}
```

**To deploy your own instance:**

1. Push your code to GitHub
2. Import the repository on [Vercel](https://vercel.com)
3. Set all environment variables in the Vercel dashboard (from your `.env`)
4. Run `npm run build:tailwind` and commit the compiled `output.css` before deploying
5. Deploy 🎉

---

## 📦 Key Dependencies

```
Django==6.0.1
psycopg2-binary==2.9.11
cloudinary==1.44.1
django-cloudinary-storage==0.3.0
whitenoise==6.12.0
python-decouple==3.8
Pillow==12.1.0
dj-database-url==3.1.0
Faker==40.1.2
django-debug-toolbar==6.1.0
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open-source. Feel free to use it for educational or personal purposes.

---

## 👤 Author

**Naim Haque** — [@naim13107](https://github.com/naim13107)
