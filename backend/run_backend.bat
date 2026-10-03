@echo off
call venv\Scripts\activate
python manage.py migrate
python manage.py seed_movies
python manage.py runserver
