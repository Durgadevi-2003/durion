# Durion Technologies Certificate Verification Platform

A production-ready Django web application for issuing, managing, verifying, and downloading certificates.

## Features
- Admin authentication and dashboard
- Certificate CRUD operations
- Public certificate verification page
- QR code generation and display
- PDF certificate generation and download
- Verification logging and search

## Setup
1. Create and activate a virtual environment.
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the app: `python manage.py runserver`

## Notes
- The project can use SQLite by default or MySQL if `DB_ENGINE=mysql` is set with matching database environment variables.
- Media files are stored under the `media/` directory.
