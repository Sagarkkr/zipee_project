# Task Management API

A Django REST Framework-based API for managing tasks with JWT authentication. Supports user registration, login, task creation, update, deletion, and filtering completed tasks.

## Features
- User Registration with JWT token authentication
- Login & Token Refresh using SimpleJWT
- Task CRUD operations (Create, Read, Update, Delete)
- Owner-only update/delete permissions
- Filter completed tasks
- Pagination & Search support
- Full Test Suite with APITestCase

## Tech Stack
- Backend: Django, Django REST Framework
- Authentication: SimpleJWT
- Database: SQLite (default), can be switched to Postgres/MySQL
- Testing: DRF APITestCase
- Filtering: django-filter

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Sagarkkr/zipee_project
```
### 2. Move into the directory
```
cd zipee_project
```
### 3. Create virtual environment
```
python -m venv env
```
### 4. Activate the virtual env
```
source env/bin/activate        # On macOS/Linux
env\Scripts\activate           # On Windows
```
### 5. Install the dependencies
```
pip install -r requirements.txt
```
### 6. Run the migration
```
python manage.py migrate
```
### 7. Create super user 
```
python manage.py createsuperuser
```
### 8. Run the server
```
python manage.py runserver
```
### 9. Run the test cases 
```
python manage.py test
```