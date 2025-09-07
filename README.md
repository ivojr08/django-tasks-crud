# Django Tasks CRUD

## Continuous learning schedule (backend Django)
- **Day 1**: CRUD with Django + templates (HTML)
- **Day 2**: API REST with DRF (serializers, viewsets, filters, toggle, tests)
- **Day 3**: (shortly)...

Example application in Django 5.2.6 to manage tasks (full CRUD):
- Create
- List (with pagination)
- Edit
- Delete (with confirmation)
- Toggle status (Pending/Completed)
- Success/Error messages
- Humanized dates

## Stack Utilizada
- Python 3.13
- Django 5.2
- SQLite (banco de dados local)

## Estrutura
- tarefas/ -> projeto Django
- tasks/ -> app principal com modelos, views e templates
- templates/ -> base e páginas HTML
- tests_api.py -> testes de API

## How to run locally
- git clone https://github.com/ivojr08/django-tasks-crud.git
- cd django-tasks-crud
- python -m venv P313venv
- source .\P313venv\Scripts\activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

## Endpoints API REST
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


