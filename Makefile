MANAGE := poetry run python manage.py

setup: install makemigrations migrate

install:
	poetry install

makemigrations:
	@$(MANAGE) makemigrations

migrate:
	@$(MANAGE) migrate

dev:
	python manage.py runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

lint:
	poetry run flake8 task_manager

test:
	@$(MANAGE) test

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

compil:
	python manage.py compilemessages