# Django Tasks CRUD

## Continuous learning schedule (backend Django)
- **Day 1**: CRUD with Django + templates (HTML)
- **Day 2**: API REST with DRF (serializers, viewsets, filters, toggle, tests)
- **Day 3**: JWT Authentication + User Protection + Login/Logout Screen + Testing
- **Day 4**: (shortly...)

Example application in Django 5.2.6 to manage tasks (full CRUD):
- Create
- List (with pagination)
- Edit
- Delete (with confirmation)
- Toggle status (Pending/Completed)
- Success/Error messages
- Humanized dates
- JWT authentication (API)
- Login/logout screen (HTML interface)

## Stack Utilizada
- Python 3.13
- Django 5.2
- Django REST Framework
- JWT (djangorestframework-simplejwt)
- SQLite (local db)

## Estrutura
- tarefas/ -> Django project
- tasks/ -> main app with models, views and templates
- templates/ -> base and pages HTML
- tests_api.py -> API tests

## How to run locally
- git clone https://github.com/ivojr08/django-tasks-crud.git
- cd django-tasks-crud
- python -m venv P313venv
- source .\P313venv\Scripts\activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

## Endpoints API REST
- POST /api/auth/token/refresh/ -> refresh token
- POST /api/auth/token/ -> login (access + refresh JWT)
- GET /api/tasks/ -> pagination list
- POST /api/tasks/ - create task (title, description, done)
- GET /api/tasks/{id}/ -> detail
- PUT /api/tasks/{id}/ -> full update
- PATCH /api/tasks/{id}/ -> partial update
- DELETE /api/tasks/{id}/ -> delete
- POST /api/tasks/{id}/toggle/ -> reverse status

## Query params
- ?done = true|false
- ?status = Pending|Completed
- ?search = word
- ?ordering = title|-title

## Tests
python manage.py test


